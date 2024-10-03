from typing import Dict

import pydantic
from langchain_core.output_parsers import JsonOutputParser
from seqia.article import Article

from ciena_llm.llm import LLM
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.impact import DroughtLLMResponse


class DroughtExtractor:
    def __init__(self, config: Dict):
        """
        Initialize the DroughtExtractor with the given configuration.

        :param config: The configuration for the DroughtExtractor.
        """
        self.ptm = PromptTemplateManager()

        # Create prompt templates
        self.drought_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["drought_extraction"]
        )
        self.drought_response_parser = JsonOutputParser(
            pydantic_object=DroughtLLMResponse
        )
        self.drought_response_parser_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["drought_response_parser"],
            format_instructions=self.drought_response_parser.get_format_instructions(),
        )

        # Create LLMs
        self.drought_llm = LLM(
            config=config["llm"],
            stage="drought_extraction",
        )
        self.drought_response_parser_llm = LLM(
            config=config["llm"],
            stage="drought_response_parser",
        )

    def extract_drought(self, article: Article) -> bool:
        text = article.get_headline_and_body(separator=".")

        # Check context length for drought prompt
        self.drought_llm.check_context_length(text, self.drought_prompt_template)

        drought_chain = self.drought_prompt_template | self.drought_llm
        drought_response = drought_chain.invoke({"text": text})
        drought_response = parse_response_bool(drought_response)

        return drought_response
