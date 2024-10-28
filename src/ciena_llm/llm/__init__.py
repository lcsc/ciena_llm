import logging

from langchain_ollama import OllamaLLM


class LLM:
    def __init__(self, config: dict, stage: str):
        """
        Initialize the LLM with the merged default and stage-specific configuration.
        :param config: Configuration dictionary containing default and stage-specific settings.
        :param stage: The stage name (e.g., "impact", "drought", etc.).
        """
        # Retrieve default and stage-specific configuration and merge them
        default_config = config.get("default", {})
        stage_config = config.get(stage, {})
        merged_config = {**default_config, **stage_config}

        self.stage = stage
        self.llm_name = merged_config["name"]
        self.llm_temperature = merged_config["temperature"]
        self.llm_context_length = merged_config["context_length"]

        # Initialize the appropriate backend LLM
        backend_name = merged_config.get("backend", "ollama")
        if backend_name == "ollama":
            self.llm = OllamaLLM(
                model=self.llm_name,
                temperature=self.llm_temperature,
                num_ctx=self.llm_context_length,
            )
        else:
            raise ValueError(f"Unsupported backend: {backend_name}")

    def log(self, message: str, data: str):
        """Log function that logs the message along with the data."""
        logging.debug("%s: %s", message, data)

    def __call__(self, text) -> str:
        """
        Call the LLM with the text and automatically log input/output with the stage.
        :param text: The input text to be passed to the LLM.
        :return: The output from the LLM.
        """
        # Check context length before calling LLM
        self.check_context_length(text)

        # Log input before calling LLM
        self.log(f"Input to LLM ({self.stage})", text)
        # Call the LLM with the input text using the `invoke` method
        response = self.llm.invoke(text)
        # Log output after LLM call
        self.log(f"Output from LLM ({self.stage})", response)
        return response

    def check_context_length(self, text):
        """
        Check if the context length of the full prompt exceeds the LLM's context length.

        :param text: The full prompt text.
        """
        num_tokens_full_prompt = self.llm.get_num_tokens(text.to_string())

        logging.debug(
            "Num. tokens (full prompt / max. context length): %s / %s",
            num_tokens_full_prompt,
            self.llm_context_length,
        )
        if num_tokens_full_prompt > self.llm_context_length:
            raise ValueError("Full prompt exceeds context length.")
