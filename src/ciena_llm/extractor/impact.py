import logging
from typing import Dict

import pydantic
from langchain_core.output_parsers import JsonOutputParser
from seqia.article import Article

from ciena_llm.llm import LLM
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.impact import ImpactLLMResponse


class ImpactExtractor:
    def __init__(self, config: Dict):
        """
        Initialize the ImpactExtractor with the given configuration.

        :param config: The configuration for the ImpactExtractor.
        """
        self.impacts = config["impacts"]

        self.ptm = PromptTemplateManager()

        # Create prompt templates
        self.impact_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["impact_extraction"]
        )
        self.impact_response_parser = JsonOutputParser(
            pydantic_object=ImpactLLMResponse
        )
        self.impact_response_parser_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["impact_response_parser"],
            format_instructions=self.impact_response_parser.get_format_instructions(),
        )

        # Create LLMs
        self.impact_llm = LLM(
            config=config["llm"],
            stage="impact_extraction",
        )
        self.impact_response_parser_llm = LLM(
            config=config["llm"],
            stage="impact_response_parser",
        )

    def extract_impact(self, article: Article) -> bool:

        # Check context length for impact prompt
        # DEBUG
        # self.impact_llm.check_context_length(text, self.drought_prompt_template)

        # Define the chain
        impact_chain = (
            self.impact_prompt_template
            | self.impact_llm
            | (lambda text: {"text": text, "impact": impact["text_en"]})
            | self.impact_response_parser_prompt_template
            | self.impact_response_parser_llm
            | self.impact_response_parser
        )

        # Get the text to analyze
        text = article.get_headline_and_body(separator=".")

        # Invoke the chain
        for impact in self.impacts:
            try:
                impact_response = impact_chain.invoke(
                    {"text": text, "impact": impact["text_en"]}
                )
                # TODO What to do if prompt is in Spanish?
            except pydantic.ValidationError as e:
                # TODO Handle this error
                logging.error("Failed to parse response: %s", e)
                raise e

            # Parse the response
            impact_response = ImpactLLMResponse(**impact_response)

            # Update the article with the extracted impact
            if impact_response.impact:
                article.impacts_aggregated.append(impact["tag"])

            logging.debug(
                "Article %s completed impact (%s) extraction",
                article.filename,
                impact["tag"],
            )

        return article
