import logging
from typing import Optional

import pydantic
from langchain_core.output_parsers import JsonOutputParser
from seqia.article import Article
from seqia.location import Location

from ciena_llm.extractor import BaseExtractor
from ciena_llm.llm_response import LLMResponseLocationList
from ciena_llm.prompt_template_manager import PromptTemplateManager


class LocationExtractor(BaseExtractor):
    def __init__(self, config):
        super().__init__(config)

        self.ptm = PromptTemplateManager()

        self.location_prompt_template = self.ptm.get_prompt_template(
            self.config["prompt"]["location"]
        )

        self.parser_location = JsonOutputParser(pydantic_object=LLMResponseLocationList)
        self.answer_extractor_location_template = self.ptm.get_prompt_template(
            self.config["prompt"]["answer_extractor"],
            format_instructions=self.parser_location.get_format_instructions(),
        )

    def extract_locations(self, article: Article) -> Optional[Article]:
        text = article.get_headline_and_body(separator=". ")

        location_chain = (
            self.location_prompt_template
            | (lambda text: self.log("Input to LLM (Location)", text))
            | self.llm
            | (lambda text: self.log("Output from LLM (Location)", text))
            | self.answer_extractor_location_template
            | (lambda text: self.log("Input to LLM (Answer Extractor)", text))
            | self.llm
            | (lambda text: self.log("Output from LLM (Answer Extractor)", text))
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
        )

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
