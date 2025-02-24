import time
from typing import Dict

from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import JsonOutputParser

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.chain.common import invoke_chain


class ResponseParsingChain(Runnable):
    def __init__(self, config, extraction_schema):
        self.step = "response_parsing"
        self.extraction_schema = extraction_schema

        self.config = config

        self.task = self.config["task"]
        self.impact_config = self.config["impacts"]
        self.pipeline_config = self.config["pipeline"][self.step]

        self.language = self.pipeline_config["prompt"]["language"]

        self.llm = LLM(config=self.config["llm"], stage=self.step)

        self.response_parser = JsonOutputParser(pydantic_object=self.extraction_schema)

        self.prompt_template = PromptTemplateManager.get_prompt_template(
            task=self.task,
            category=self.step,
            language=self.language,
            output="json",
            format_instructions=self.extraction_schema.get_format_instructions(),
            impacts=PromptTemplateManager.get_impact_names_text(
                self.impact_config, self.language
            ),
            impact_descriptions=PromptTemplateManager.get_impact_descriptions_text(
                self.impact_config, self.language
            ),
        )

        self.chain = self.prompt_template | self.llm | self.response_parser

        self.prompts = {
            "extraction_impact": {
                "task": self.task,
                "step": self.step,
                "language": self.language,
                "output": "json",
                "template": self.prompt_template.pretty_repr(),
            },
        }

        self.parsing_errors = {}
        self.execution_times = {}

    def invoke(self, input_data: Dict, *args, **kwargs):
        """
        Parse the response from the LLM using the response parsing prompt template.

        :param input_data: The input data for the response parsing chain.
        :return: Parsed response.
        """

        input_text = input_data.get("text")
        article_id = input_data.get("article_id")

        start_time = time.time()

        # Invoke response parsing chain
        (response, parsing_error) = invoke_chain(
            self.chain,
            input_text,
            self.extraction_schema,
        )

        execution_time = time.time() - start_time

        if parsing_error:
            self.parsing_errors[article_id] = parsing_error

        self.execution_times[article_id] = execution_time

        return {
            "article_id": article_id,
            "output": response,
        }
