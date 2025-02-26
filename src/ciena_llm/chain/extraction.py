import time
from typing import Dict

from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import JsonOutputParser

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.chain.common import invoke_chain


class ExtractionChain(Runnable):
    def __init__(self, config, extraction_schema):
        self.step = "extraction"
        self.extraction_schema = extraction_schema

        self.config = config

        self.task = self.config["task"]
        self.event_config = self.config["event"]
        self.impact_config = self.config["impacts"]
        self.pipeline_step_config = self.config["pipeline"][self.step]
        self.step_prompt_config = self.pipeline_step_config["prompt"]
        self.language = self.pipeline_step_config["prompt"]["language"]

        # If the response parsing pipeline step is disabled in the config,
        # the extraction chain will have to parse the response
        self.response_parsing = not (
            self.config["pipeline"]["response_parsing"]["enable"]
        )

        self.llm = LLM(config=self.config["llm"], stage=self.step)

        # TODO do better?
        if self.response_parsing:
            self.response_parser = JsonOutputParser(
                pydantic_object=self.extraction_schema
            )

            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task=self.task,
                **self.step_prompt_config,
                output="json",
                # TODO which one is better?
                # format_instructions=self.response_parser.get_format_instructions(),
                format_instructions=self.extraction_schema.get_format_instructions(),
                impacts=PromptTemplateManager.get_impact_names_text(
                    self.impact_config, self.language
                ),
                impact_descriptions=PromptTemplateManager.get_impact_descriptions_text(
                    self.impact_config, self.language
                ),
            )

            self.chain = self.prompt_template | self.llm | self.response_parser

        else:
            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task=self.task,
                **self.step_prompt_config,
                output="text",
                # TODO always pass as parameters?
                impacts=PromptTemplateManager.get_impact_names_text(
                    self.impact_config, self.language
                ),
                impact_descriptions=PromptTemplateManager.get_impact_descriptions_text(
                    self.impact_config, self.language
                ),
            )

            self.chain = self.prompt_template | self.llm

        self.prompts = {
            f"extraction_{self.task}": {
                "task": self.task,
                **self.step_prompt_config,
                "output": "json" if self.response_parsing else "text",
                "template": self.prompt_template.pretty_repr(),
            },
        }

        self.parsing_errors = {}
        self.execution_times = {}

    def invoke(self, input_data: Dict, *args, **kwargs):
        """
        Extract the information needed from the provided text using the LLM and extraction prompt template.

        :param input_data: The input data for the extraction chain.
        :return: Extracted information.
        """

        input_text = input_data.get("text")
        article_id = input_data.get("article_id")

        start_time = time.time()

        # Invoke extraction chain
        (response, parsing_error) = invoke_chain(
            self.chain,
            input_text,
            self.extraction_schema,
            response_parsing=self.response_parsing,
        )

        execution_time = time.time() - start_time

        if parsing_error:
            self.parsing_errors[article_id] = parsing_error

        self.execution_times[article_id] = execution_time

        return {
            "article_id": article_id,
            "output": response,
        }
