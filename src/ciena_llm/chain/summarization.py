import time
from typing import Dict

from langchain_core.runnables.base import Runnable

from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.llm import LLM


class SummarizationChain(Runnable):
    def __init__(self, stage, config, llm_config):
        self.pipeline_step = "summarization"
        self.stage = stage

        self.llm_config = llm_config

        self.config = config
        self.prompt_config = self.config["prompt"]
        self.language = self.config["prompt"]["language"]

        self.llm = LLM(
            config=self.llm_config, stage=f"{self.stage}-{self.pipeline_step}"
        )

        self.prompt_template = PromptTemplateManager.get_prompt_template(
            stage=self.stage,
            **self.prompt_config,
        )

        self.chain = self.prompt_template | self.llm

        self.prompts = {
            "stage": self.stage,
            "pipeline_step": self.pipeline_step,
            **self.prompt_config,
            "template": self.prompt_template.pretty_repr(),
        }

        self.execution_times = {}

    def invoke(self, input_data: Dict, *args, **kwargs):
        """
        Summarize the provided text using the LLM and summarization prompt template.

        :param input_data: The input data for the summarization chain.
        :return: Summarized text.
        """

        input_text = input_data.get("text")
        article_id = input_data.get("article_id")

        start_time = time.time()

        # Invoke summarization chain
        summarized_text = self.chain.invoke({"text": input_text})

        execution_time = time.time() - start_time

        self.execution_times[article_id] = execution_time

        return {
            "article_id": article_id,
            "output": summarized_text.strip(),
        }
