import time
from typing import Dict

from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import JsonOutputParser

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.chain.common import invoke_chain


class ExtractionChain(Runnable):
    def __init__(
        self,
        stage,
        config,
        extraction_schema,
        llm_config,
        event_config=None,
        impact_config=None,
        response_parsing_enable=False,
    ):
        self.stage = stage
        self.pipeline_step = "extraction"

        self.llm_config = llm_config
        self.extraction_schema = extraction_schema
        self.event_config = event_config
        self.impact_config = impact_config

        self.config = config
        self.prompt_config = self.config["prompt"]
        self.language = self.config["prompt"]["language"]
        # If the response parsing pipeline step is disabled in the config, the extraction chain will have to parse the response
        self.response_parsing_enable = not response_parsing_enable

        # TODO change stage naming
        self.llm = LLM(config=self.llm_config, stage=self.pipeline_step)

        # TODO do better?
        if self.response_parsing_enable:
            self.response_parser = JsonOutputParser(
                pydantic_object=self.extraction_schema
            )

            # TODO change task/stage naming
            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task=self.stage,
                **self.prompt_config,
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
            # TODO change task/stage naming
            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task=self.stage,
                **self.prompt_config,
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
            "stage": self.stage,
            "pipeline_step": self.pipeline_step,
            **self.prompt_config,
            "output": "json" if self.response_parsing_enable else "text",
            "template": self.prompt_template.pretty_repr(),
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
            response_parsing=self.response_parsing_enable,
        )

        execution_time = time.time() - start_time

        if parsing_error:
            self.parsing_errors[article_id] = parsing_error

        self.execution_times[article_id] = execution_time

        return {
            "article_id": article_id,
            "output": response,
        }
