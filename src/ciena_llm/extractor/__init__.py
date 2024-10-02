import logging

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


class BaseExtractor:
    def __init__(self, config):

        self.config = config

        self.llm_name = self.config["llm"]["name"]
        self.llm_temperature = self.config["llm"]["temperature"]
        self.llm_context_length = self.config["llm"]["context_length"]

        self.llm = OllamaLLM(
            model=self.llm_name,
            temperature=self.llm_temperature,
            num_ctx=self.llm_context_length,
        )

        # TODO generalize into base class:
        # - prompt template manager for extraction and parsing
        # - others...

    def log(self, stage: str, data: str):
        logging.debug("%s: %s", stage, data)
        return data

    def check_context_length(self, text: str, prompt_template: PromptTemplate):
        num_tokens_text = self.llm.get_num_tokens(text)
        full_prompt = prompt_template.invoke({"text": text})
        num_tokens_full_prompt = self.llm.get_num_tokens(full_prompt.to_string())

        logging.debug(
            "Num. tokens (text / full prompt / max. context lenght): %s / %s / %s",
            num_tokens_text,
            num_tokens_full_prompt,
            self.llm_context_length,
        )
        if num_tokens_full_prompt > self.llm_context_length:
            logging.warning("Full prompt exceeds context length.")
