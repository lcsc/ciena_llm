import logging
from typing import Dict

import pydantic
from langchain_core.output_parsers import JsonOutputParser
from seqia.article import Article

from ciena_llm.llm import LLM
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.boolean import BooleanLLMResponse


class DroughtClassifier:
    def __init__(self, config: Dict):
        """
        Initialize the DroughtClassifier with the given configuration.

        :param config: The configuration for the DroughtClassifier.
        """
        self.ptm = PromptTemplateManager()

        # Create prompt templates
        self.drought_classification_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["drought_classification"]
        )
        self.drought_response_parser = JsonOutputParser(
            pydantic_object=BooleanLLMResponse
        )
        self.drought_response_parser_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["drought_response_parser"],
            format_instructions=self.drought_response_parser.get_format_instructions(),
        )

        # Create LLMs
        self.drought_llm = LLM(
            config=config["llm"],
            stage="drought_classification",
        )
        self.drought_response_parser_llm = LLM(
            config=config["llm"],
            stage="drought_response_parser",
        )

        # Save prompts
        self.prompts = {
            "drought_classification": {
                "name": config["prompt"]["drought_classification"],
                "template": self.drought_classification_prompt_template.pretty_repr(),
            },
            "drought_response_parser": {
                "name": config["prompt"]["drought_response_parser"],
                "template": self.drought_response_parser_prompt_template.pretty_repr(),
            },
        }

    def classify(self, article: Article) -> Article:

        # Define the chain
        drought_chain = (
            self.drought_classification_prompt_template
            | self.drought_llm
            | self.drought_response_parser_prompt_template
            | self.drought_response_parser_llm
            | self.drought_response_parser
        )

        # Get the text to analyze
        text = article.get_headline_and_body(separator=". ")

        # Invoke the chain
        try:
            drought_response = drought_chain.invoke({"text": text})
        except pydantic.ValidationError as e:
            # TODO Handle this error
            logging.error("Failed to parse response: %s", e)
            raise e

        # Parse the response
        drought_response = BooleanLLMResponse(**drought_response)

        # Update the article with the extracted drought information
        article.drought = drought_response.response

        logging.debug("Article %s completed drought classification", article.filename)

        return article
