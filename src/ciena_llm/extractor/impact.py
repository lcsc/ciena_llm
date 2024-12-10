import logging
from typing import Dict

import pydantic
from langchain_core.output_parsers import JsonOutputParser
from seqia.article import Article

from ciena_llm.llm import LLM
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.boolean import BooleanLLMResponse


class ImpactExtractor:
    def __init__(self, config: Dict):
        """
        Initialize the ImpactExtractor with the given configuration.

        :param config: The configuration for the ImpactExtractor.
        """
        self.impacts = config["impacts"]

        self.ptm = PromptTemplateManager()

        # Create response parser
        self.impact_response_parser = JsonOutputParser(
            pydantic_object=BooleanLLMResponse
        )

        self.impact_reponse_parser_enable = (
            config["prompt"]["impact_response_parser"] is not None
        )

        # Create prompt templates
        if self.impact_reponse_parser_enable:
            # - Impact extraction
            self.impact_extraction_prompt_template = self.ptm.get_prompt_template(
                config["prompt"]["impact_extraction"]
            )
            # - Impact response parser
            self.impact_response_parser_prompt_template = self.ptm.get_prompt_template(
                config["prompt"]["impact_response_parser"],
                format_instructions=self.impact_response_parser.get_format_instructions(),
            )
        else:
            # - Impact extraction + response parser
            self.impact_extraction_prompt_template = self.ptm.get_prompt_template(
                config["prompt"]["impact_extraction"],
                # format_instructions=self.impact_response_parser.get_format_instructions(),  # TODO how to do if there are not format instructions partial variable
            )

        # Create LLMs
        # - Impact extraction
        self.impact_llm = LLM(
            config=config["llm"],
            stage="impact_extraction",
        )
        if self.impact_reponse_parser_enable:
            # - Impact response parser
            self.impact_response_parser_llm = LLM(
                config=config["llm"],
                stage="impact_response_parser",
            )

        # Save prompts
        self.prompts = {
            "impact_extraction": {
                "name": config["prompt"]["impact_extraction"],
                "template": self.impact_extraction_prompt_template.pretty_repr(),
            }
        }
        if self.impact_reponse_parser_enable:
            self.prompts.update(
                {
                    "impact_response_parser": {
                        "name": config["prompt"]["impact_response_parser"],
                        "template": self.impact_response_parser_prompt_template.pretty_repr(),
                    }
                }
            )

    def extract_impact(self, article: Article) -> bool:

        # Define the chain
        if self.impact_reponse_parser_enable:

            impact_chain = (
                self.impact_extraction_prompt_template
                | self.impact_llm
                | (
                    lambda text: {
                        "text": text,
                        "impact": impact["text_es"],  # TODO language??
                    }
                )
                | self.impact_response_parser_prompt_template
                | self.impact_response_parser_llm
                | self.impact_response_parser
            )
        else:
            impact_chain = (
                self.impact_extraction_prompt_template
                | self.impact_llm
                | self.impact_response_parser
            )

        # Get the text to analyze
        text = article.get_headline_and_body(separator=".")

        # Invoke the chain
        for impact in self.impacts:
            try:
                impact_response = impact_chain.invoke(
                    {
                        "text": text,
                        "impact": impact["text_es"],  # TODO language??
                        "impact_description": impact[
                            "description_es"
                        ],  # TODO language??
                    }
                )
                # TODO What to do if prompt is in Spanish?
            except pydantic.ValidationError as e:
                # TODO Handle this error
                logging.error("Failed to parse response: %s", e)
                raise e

            # Parse the response
            impact_response = BooleanLLMResponse(**impact_response)

            # Update the article with the extracted impact
            if impact_response.response:
                article.impacts_aggregated.append(impact["tag"])

            logging.debug(
                "Article %s completed impact (%s) extraction",
                article.filename,
                impact["tag"],
            )

        return article
