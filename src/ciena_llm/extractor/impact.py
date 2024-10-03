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
        text = article.get_headline_and_body(separator=".")

        # Check context length for impact prompt
        self.impact_llm.check_context_length(text, self.impact_prompt_template)

        impact_chain = self.impact_prompt_template | self.impact_llm
        impact_response = impact_chain.invoke({"text": text})
        impact_response = parse_response_bool(impact_response)

        return impact_response
