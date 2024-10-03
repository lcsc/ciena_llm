import logging
from typing import Dict

import pydantic
from langchain_core.output_parsers import JsonOutputParser
from seqia.article import Article
from seqia.location import Location

from ciena_llm.llm import LLM
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.location import LocationListLLMResponse


class LocationExtractor:
    def __init__(self, config: Dict):
        """
        Initialize the LocationExtractor with the given configuration.

        :param config: The configuration for the LocationExtractor.
        """
        self.ptm = PromptTemplateManager()

        # Create prompt templates
        # - Location extraction
        self.location_extraction_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["location_extraction"]
        )
        # - Location response parser
        self.location_response_parser = JsonOutputParser(
            pydantic_object=LocationListLLMResponse
        )
        self.location_response_parser_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["location_response_parser"],
            format_instructions=self.location_response_parser.get_format_instructions(),
        )

        # Create LLMs
        # - Location extraction
        self.location_extraction_llm = LLM(
            config=config["llm"], stage="location_extraction"
        )
        # - Location response parser
        self.location_response_parser_llm = LLM(
            config=config["llm"], stage="location_response_parser"
        )

    def extract_locations(self, article: Article) -> Article:
        """
        Extract locations from the given article.

        :param article: The article to extract locations from.

        :return: The article with the extracted locations.
        """

        # Define the chain
        location_chain = (
            self.location_extraction_prompt_template
            | self.location_extraction_llm
            | self.location_response_parser_prompt_template
            | self.location_response_parser_llm
            | self.location_response_parser
        )

        # Get the text from the article to input to the chain
        text = article.get_headline_and_body(separator=". ")

        # Invoke the chain
        try:
            location_response = location_chain.invoke({"text": text})
        except pydantic.ValidationError as e:
            # TODO Handle this error
            logging.error("Failed to parse response: %s", e)
            raise e

        # TODO FIX Deprecated
        location_response: LocationListLLMResponse = LocationListLLMResponse.parse_obj(
            location_response
        )

        # Add the extracted locations to the article
        article.locations_aggregated = [
            Location(
                name=location.location_name,
                type=location.location_type,
                start=None,  # TODO anything else?
                end=None,
            )
            for location in location_response.locations
        ]

        return article
