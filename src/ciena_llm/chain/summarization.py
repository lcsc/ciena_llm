from langchain_core.runnables.base import Runnable

from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.llm import LLM


class SummarizationChain(Runnable):
    def __init__(self, config):
        self.step = "summarization"
        self.config = config

        self.task = config["task"]

        self.pipeline_config = self.config["pipeline"][self.step]
        self.language = self.pipeline_config["prompt"]["language"]

        self.llm = LLM(config=self.config["llm"], stage=self.step)

        self.prompt_template = PromptTemplateManager.get_prompt_template(
            category=self.step,
            language=self.language,
        )

        self.chain = self.prompt_template | self.llm

        self.prompts = {
            "extraction_impact": {
                "task": self.task,
                "step": self.step,
                "language": self.language,
                "template": self.prompt_template.pretty_repr(),
            },
        }

    def invoke(self, input_text: str, *args, **kwargs):
        """
        Summarize the provided text using the LLM and summarization prompt template.

        :param text: The input text (article).
        :return: Summarized text.
        """

        # Invoke summarization chain
        summarized_text = self.chain.invoke({"text": input_text})
        summarized_text = summarized_text.strip()

        return summarized_text
