import logging
from typing import Optional

import pydantic
from langchain_core.output_parsers import JsonOutputParser
from seqia.article import Article
from seqia.location import Location

from ciena_llm.llm import LLM
from ciena_llm.llm_response import LLMResponseLocationList
from ciena_llm.prompt_template_manager import PromptTemplateManager


class LocationExtractor:
    def __init__(self, config):
        self.ptm = PromptTemplateManager()

        self.location_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["location"]
        )

        self.parser_location = JsonOutputParser(pydantic_object=LLMResponseLocationList)
        self.answer_extractor_location_template = self.ptm.get_prompt_template(
            config["prompt"]["answer_extractor"],
            format_instructions=self.parser_location.get_format_instructions(),
        )

        # Create LLMs for different stages
        self.location_llm = LLM(config=config["llm"], stage="location")
        self.answer_extractor_llm = LLM(config=config["llm"], stage="answer_extractor")

    def extract_locations(self, article: Article) -> Optional[Article]:
        text = article.get_headline_and_body(separator=". ")

        location_chain = (
            self.location_prompt_template
            | self.location_llm
            | self.answer_extractor_location_template
            | self.answer_extractor_llm
            | self.parser_location
        )

        try:
            location_response = location_chain.invoke({"text": text})
        except pydantic.ValidationError as e:
            logging.error("Failed to parse response: %s", e)
            raise e

        logging.debug("Location Response: %s", location_response)

        location_response: LLMResponseLocationList = LLMResponseLocationList.parse_obj(
            location_response
        )  # TODO FIX Deprecated

        locations = []
        for location in location_response.locations:
            locations.append(
                Location(
                    name=location.location_name,
                    type=location.location_type,
                    start=None,
                    end=None,
                )
            )
        article.locations_aggregated = locations

        return article
