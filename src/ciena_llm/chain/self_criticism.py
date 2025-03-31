import time
from typing import Dict

from langchain_core.runnables.base import Runnable

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager


# TODO
class SelfCriticismChain(Runnable):
    def __init__(
        self,
        stage,
        config,
        llm_config,
        extraction_schema,
    ):
        self.stage = stage
        self.pipeline_step = "self_criticism"

        self.llm_config = llm_config
        self.extraction_schema = extraction_schema

        self.structured_output_mode = self.llm_config.get("structured_output_mode")

        self.config = config
        self.prompt_config = self.config["prompt"]
        self.language = self.config["prompt"]["language"]

        self.prompt_template = PromptTemplateManager.get_prompt_template(
            **self.prompt_config,
            output="json" if self.structured_output_mode == "prompt" else "text",
            format_instructions=(
                self.extraction_schema.format_instructions_as_json()
                if self.structured_output_mode == "prompt"
                else None
            ),
        )

        self.llm = LLM(
            config=self.llm_config,
            stage=f"{self.stage}-{self.pipeline_step}",
            extraction_schema=self.extraction_schema,
        )

        self.chain = self.prompt_template | self.llm

        self.prompts = {
            "stage": self.stage,
            "pipeline_step": self.pipeline_step,
            **self.prompt_config,
            "output": "json" if self.extraction_schema is not None else "text",
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

        # input_text = input_data.get("text")
        article_id = input_data.get("article_id")
        input_prompt = input_data.get("prompt")
        input_response = input_data.get("response")

        start_time = time.time()

        # Invoke extraction chain
        (response, parsing_error) = self.chain.invoke(
            {"prompt": input_prompt, "response": input_response}
        )

        execution_time = time.time() - start_time

        if parsing_error:
            self.parsing_errors[article_id] = parsing_error

        self.execution_times[article_id] = execution_time

        return {
            "article_id": article_id,
            "output": response,
        }
