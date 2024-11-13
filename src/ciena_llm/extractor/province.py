import logging
from typing import Dict

import pydantic
from langchain_core.output_parsers import JsonOutputParser
from seqia.article import Article

from ciena_llm.llm import LLM
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.province import ProvinceLLMResponse


class ProvinceExtractor:
    def __init__(self, config: Dict):
        """
        Initialize the ProvinceExtractor with the given configuration.

        :param config: The configuration for the ProvinceExtractor.
        """
        self.ptm = PromptTemplateManager()

        # Create response parser
        self.province_response_parser = JsonOutputParser(
            pydantic_object=ProvinceLLMResponse
        )

        self.province_response_parser_enable = (
            config["prompt"]["province_response_parser"] is not None
        )

        # Create prompt templates
        if self.province_response_parser_enable:
            # - Province extraction
            self.province_extraction_prompt_template = self.ptm.get_prompt_template(
                config["prompt"]["province_extraction"]
            )
            # - Province response parser
            self.province_response_parser_prompt_template = self.ptm.get_prompt_template(
                config["prompt"]["province_response_parser"],
                format_instructions=self.province_response_parser.get_format_instructions(),
            )
        else:
            # - Province extraction + response parser
            self.province_extraction_prompt_template = self.ptm.get_prompt_template(
                config["prompt"]["province_extraction"],
                format_instructions=self.province_response_parser.get_format_instructions(),  # TODO how to do if there are not format instructions partial variable
            )

        # Create LLMs
        # - Province extraction
        self.province_extraction_llm = LLM(
            config=config["llm"], stage="province_extraction"
        )
        if self.province_response_parser_enable:
            # - Province response parser
            self.province_response_parser_llm = LLM(
                config=config["llm"], stage="province_response_parser"
            )

        # Save prompts
        self.prompts = {
            "province_extraction": {
                "name": config["prompt"]["province_extraction"],
                "template": self.province_extraction_prompt_template.pretty_repr(),
            },
        }
        if self.province_response_parser_enable:
            self.prompts.update(
                {
                    "province_response_parser": {
                        "name": config["prompt"]["province_response_parser"],
                        "template": self.province_response_parser_prompt_template.pretty_repr(),
                    },
                }
            )

    def extract_provinces(self, article: Article) -> Article:
        """
        Extract provinces from the given article.

        :param article: The article to extract provinces from.

        :return: The article with the extracted provinces.
        """

        # Define the chain
        if self.province_response_parser_enable:
            province_chain = (
                self.province_extraction_prompt_template
                | self.province_extraction_llm
                | self.province_response_parser_prompt_template
                | self.province_response_parser_llm
                | self.province_response_parser
            )
        else:
            province_chain = (
                self.province_extraction_prompt_template
                | self.province_extraction_llm
                | self.province_response_parser
            )

        # Get the text from the article to input to the chain
        text = article.get_headline_and_body(separator=". ")

        # Invoke the chain
        try:
            province_response = province_chain.invoke({"text": text})
        except pydantic.ValidationError as e:
            # TODO Handle this error
            logging.error("Failed to parse response: %s", e)
            raise e

        # Parse the response
        if isinstance(province_response, list):
            province_response = {"response": province_response}

        province_response_data: ProvinceLLMResponse = ProvinceLLMResponse(
            **province_response
        )

        # Update the article with the extracted provinces
        article.provinces = province_response_data.response

        logging.debug("Article %s completed province extraction", article.filename)

        return article
