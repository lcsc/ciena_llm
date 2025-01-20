import logging

import pydantic
from pydantic import ValidationError

from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.province import ProvinceLLMResponse


class ProvinceExtractionChain(Runnable):
    def __init__(self, config):
        self.step = "extraction"
        self.config = config

        self.pipeline_config = self.config["pipeline"][self.step]

        self.language = self.pipeline_config["prompt"]["language"]

        # If the response parsing pipeline step is disabled in the config, the extraction chain will have to parse the response
        self.response_parsing = not (
            self.config["pipeline"]["response_parsing"]["enable"]
        )

        self.llm = LLM(config=self.config["llm"], stage=self.step)

        # TODO do better?
        if self.response_parsing:
            self.response_parser = JsonOutputParser(pydantic_object=ProvinceLLMResponse)

            # JSON format instructions for the model
            format_instructions = f"""
```json 
{{
    "response": [
        "province name 1",
        "province name 2",
    ]
}}
```
"""

            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task="province",
                step="extraction",
                language=self.language,
                output="json",
                format_instructions=format_instructions,
            )

            self.chain = self.prompt_template | self.llm | self.response_parser

        else:
            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task="province",
                step="extraction",
                language=self.language,
                output="text",
            )

            self.chain = self.prompt_template | self.llm

    def invoke(self, input: str, *args, **kwargs):

        if self.response_parsing:
            try:
                # Invoke the chain
                output = self.chain.invoke({"text": input})

                # Parse the response
                return ProvinceLLMResponse(**output)

            except pydantic.ValidationError as e:
                logging.error(
                    "pydantic.ValidationError: Failed to parse response: %s", e
                )
                print(f"OUTPUT: {output}")
                # TODO Handle this error
                # raise e
                return ProvinceLLMResponse(**{"response": []})

            except OutputParserException as e:
                logging.error("OutputParserException: Failed to parse response: %s", e)
                # TODO Handle this error
                # raise e
                return ProvinceLLMResponse(**{"response": []})

        else:
            output = self.chain.invoke({"text": input})
            return output
