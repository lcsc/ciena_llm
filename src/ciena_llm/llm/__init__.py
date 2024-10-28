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
        self.llm_num_predict_tokens = merged_config["num_predict_tokens"]

        # Initialize the appropriate backend LLM
        backend_name = merged_config.get("backend", "ollama")
        if backend_name == "ollama":
            self.llm = OllamaLLM(
                model=self.llm_name,
                temperature=self.llm_temperature,
                num_ctx=self.llm_context_length,
                num_predict=self.llm_num_predict_tokens,
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
        self.check_context_length(text.to_string())

        # Log input before calling LLM
        self.log(f"Input to LLM ({self.stage})", text)
        # Call the LLM with the input text using the `invoke` method
        response = self.llm.invoke(text)
        # Log output after LLM call
        self.log(f"Output from LLM ({self.stage})", response)

        # Check predicted tokens after calling LLM
        self.check_predicted_tokens(response)

        return response

    def check_context_length(self, text):
        """
        Check if the number of tokens of the text exceeds the LLM's context length.

        :param text: The text to check.
        """
        num_tokens_full_prompt = self.llm.get_num_tokens(text)

        logging.debug(
            "Num. tokens (full prompt / max. context length): %s / %s",
            num_tokens_full_prompt,
            self.llm_context_length,
        )
        if num_tokens_full_prompt > self.llm_context_length:
            raise ValueError("Full prompt exceeds context length.")

    def check_predicted_tokens(self, text):
        """
        Check if the number of tokens predicted by the LLM matches the max number of predicted tokens allowed.

        :param text: The text to check.
        """

        num_tokens_predicted = self.llm.get_num_tokens(text)

        logging.debug(
            "Num. tokens predicted / max. predicted tokens: %s / %s",
            num_tokens_predicted,
            self.llm_num_predict_tokens,
        )
        if num_tokens_predicted >= self.llm_num_predict_tokens:
            logging.warning(
                "Number of predicted tokens matches the maximum allowed. The generation might have been interrupted and may not have finished correctly."
            )
