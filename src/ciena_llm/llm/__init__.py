import logging
from typing import Union, Tuple, Dict
from textwrap import dedent

import pydantic
from pydantic import BaseModel
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama

# from langchain_core.globals import set_verbose, set_debug
# set_verbose(True)
# set_debug(True)


class LLM:
    def __init__(
        self, config: dict, pipeline_step: str, extraction_schema: BaseModel = None
    ):
        """
        Initialize the LLM with the specific configuration.

        :param config: Configuration dictionary containing settings.
        :param pipeline_step: The pipeline_step name (e.g., "impact", "drought", etc.).
        :param extraction_schema: The extraction schema to be used for parsing the LLM output.
        """

        self.pipeline_step = pipeline_step
        self.config = config
        self.extraction_schema = extraction_schema

        self.llm_name = self.config.get("name")
        self.llm_temperature = self.config.get("temperature")
        self.llm_context_length = self.config.get("context_length")
        self.llm_num_predict_tokens = self.config.get("num_predict_tokens")
        self.llm_seed = int(self.config.get("seed"))

        self.structured_output_mode = self.config.get("structured_output_mode")

        think_mode = self.config.get("thinking", None)
        mKwArgs = self.config.get("model_kwargs",None)
        if think_mode is not None:
            print(f"LLM Thinking mode enabled: {think_mode}")
        if mKwArgs is not None:
            print(f"Model KwArgs: {mKwArgs}")

        # Initialize the appropriate backend LLM
        backend_name = self.config.get("backend", "ollama")
        if backend_name == "ollama":
            self.llm = ChatOllama(
                model=self.llm_name,
                temperature=self.llm_temperature,
                num_ctx=self.llm_context_length,
                num_predict=self.llm_num_predict_tokens,
                seed=self.llm_seed,
                reasoning=think_mode,
                model_kwargs=mKwArgs
            )
        else:
            raise ValueError(f"Unsupported backend: {backend_name}")

        self.llm_structured = None

        # Initialize the structured output LLM if an schema is provided
        if self.extraction_schema is not None:
            if self.structured_output_mode == "prompt":
                self.response_parser = JsonOutputParser(
                    pydantic_object=self.extraction_schema
                )
                # TODO unused but in condition
                self.llm_structured = self.llm | self.response_parser
            elif self.structured_output_mode == "tool":
                self.llm_structured = self.llm.with_structured_output(
                    self.extraction_schema, include_raw=True
                )

    def log(self, message: str, data: str):
        """Log function that logs the message along with the data."""
        logging.debug("%s: %s", message, data)

    def log_tool_call(self, message: str, data: dict):
        """Log function that logs the message along with the data for structured output."""
        formatted_data = dedent(
            f"""
            - LLM Output (text):
            '{data["raw"].content}'
            {f"- Tool Call: {data['raw'].tool_calls[0]['name']}" if data['parsed'] else ""}
            {f"- Tool Call Args: {data['raw'].tool_calls[0]['args']}" if data['parsed'] else ""}
            - Parsed LLM Output (JSON):
            {data["parsed"]}
            {f"- Parsing Error: {str(data['parsing_error'])}" if data["parsing_error"] else ""}
            """
        )
        logging.debug(
            "%s (with tool usage for JSON Structured Output): %s",
            message,
            formatted_data,
        )

    def invoke_llm(
        self, text: str
    ) -> Tuple[Union[str, BaseModel], str, Union[Dict, None]]:
        # Call the LLM with the input text
        response = self.llm.invoke(text)
        # Obtain the response content
        response = response.content
        # Log output after LLM call
        self.log(f"Output from LLM ({self.pipeline_step})", response)

        return (
            response,
            response,
            {},
        )

    def invoke_structured_llm_with_tool(
        self, text: str
    ) -> Tuple[Union[str, BaseModel], str, Union[Dict, None]]:
        # Call the structured output LLM with the input text
        response = self.llm_structured.invoke(text)
        # Obtain the response content
        response_content = response["raw"].content
        # Log structured output
        self.log_tool_call(f"Output from LLM ({self.pipeline_step})", response)
        # Check for parsing errors
        if response["parsed"] is None:
            response_parsing_error = {}
            if response["parsing_error"] is not None:
                response_parsing_error = {
                    "exception": str(response["parsing_error"]),
                    "output": str(response),
                }
            response = self.extraction_schema.default_response()
        else:
            response_parsing_error = {}
            response = response["parsed"]

        return (
            response,
            response_content,
            response_parsing_error,
        )

    def invoke_structured_llm_with_prompt(
        self, text: str
    ) -> Tuple[Union[str, BaseModel], str, Union[Dict, None]]:
        try:
            # Invoke the LLM
            response = self.llm.invoke(text)
            response_content = response.content

            # Log output after LLM call
            self.log(f"Output from LLM ({self.pipeline_step})", response_content)

            # Invoke the response parser
            response = self.response_parser.invoke(response)

            # Parse the response to a dictionary if needed
            if not isinstance(response, dict) and hasattr(
                self.extraction_schema, "normalize_response_format"
            ):
                response = self.extraction_schema.normalize_response_format(response)

            # Parse the response
            parsed_response = self.extraction_schema(**response)

            return (
                parsed_response,
                response_content,
                {},
            )
        except pydantic.ValidationError as e:
            logging.error("pydantic.ValidationError: Failed to parse response: %s", e)
            # Return the default error response
            return (
                self.extraction_schema.default_response(),
                response_content,
                {"exception": str(e), "output": response_content},
            )

        except OutputParserException as e:
            logging.error("OutputParserException: Failed to parse response: %s", e)
            # Return the default error response
            return (
                self.extraction_schema.default_response(),
                "",
                {"exception": str(e)},
            )
        except TypeError as e:
            logging.error("TypeError: Failed to parse response: %s", e)
            # Return the default error response
            return (
                self.extraction_schema.default_response(),
                "",
                {"exception": str(e)},
            )

    def __call__(self, text) -> Tuple[Union[str, BaseModel], Union[Dict, None]]:
        """
        Call the LLM with the text and automatically log input/output with the stage.

        :param text: The input text to be passed to the LLM.
        :return: The response from the LLM and the parsing error (if any).
        """
        # Check context length before calling LLM
        self.check_context_length(text.to_string())

        # Log input before calling LLM
        self.log(f"Input to LLM ({self.pipeline_step})", text)

        # Call the LLM with the input text using the `invoke` method
        if self.llm_structured is None:
            response, response_content, response_parsing_error = self.invoke_llm(text)
        else:
            if self.structured_output_mode == "tool":
                response, response_content, response_parsing_error = (
                    self.invoke_structured_llm_with_tool(text)
                )
            else:  #  self.structured_output_mode == "prompt":
                response, response_content, response_parsing_error = (
                    self.invoke_structured_llm_with_prompt(text)
                )

        # Check predicted tokens after calling LLM
        self.check_predicted_tokens(response_content)

        return (response, response_parsing_error)

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
            logging.warning(
                "Full prompt exceeds context length. The LLM may not be able to process the input correctly."
            )
            # raise ValueError("Full prompt exceeds context length.")

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
