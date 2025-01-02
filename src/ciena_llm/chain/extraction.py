import logging

import pydantic
from pydantic import ValidationError

from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.impact import ImpactLLMResponse


class ExtractionChain(Runnable):
    def __init__(self, config):
        self.step = "extraction"
        self.config = config

        # TODO parametrize impacts?
        # TODO for impacts only?
        self.impact_config = self.config["impacts"]
        self.pipeline_config = self.config["pipeline"][self.step]

        self.language = self.pipeline_config["prompt"]["language"]

        self.impact_names = [i[f"text_{self.language}"] for i in self.impact_config]
        self.impact_descriptions = [
            i[f"description_{self.language}"] for i in self.impact_config
        ]
        self.impact_names_text = ", ".join(self.impact_names)
        self.impact_descriptions_text = ", ".join(
            [
                f"{impact}: {description}"
                for impact, description in zip(
                    self.impact_names, self.impact_descriptions
                )
            ]
        )

        self.llm = LLM(config=self.config["llm"], stage=self.step)

        self.response_parser = JsonOutputParser(pydantic_object=ImpactLLMResponse)

        # JSON format instructions for the model
        format_instructions = f"""
```json 
{{
    "drought": <true or false>,
    {"\n".join([f"\"{i['tag']}\": <true or false>," for i in self.impact_config])}
}}
```
        """

        self.extraction_prompt_template = PromptTemplateManager.get_prompt_template(
            task="impact",
            step="multi_classification",
            language=self.language,
            category="description",
            output="json",  # TODO from config
            format_instructions=format_instructions,
        )

        self.chain = self.extraction_prompt_template | self.llm | self.response_parser

    def invoke(self, input: str, *args, **kwargs):

        try:
            # Invoke the chain
            output = self.chain.invoke(
                {
                    "text": input,
                    "impacts": self.impact_names_text,
                    "impact_descriptions": self.impact_descriptions_text,
                }
            )

            # Parse the response
            return ImpactLLMResponse(**output)

        except pydantic.ValidationError as e:
            logging.error("pydantic.ValidationError: Failed to parse response: %s", e)
            print(f"OUTPUT: {output}")
            # TODO Handle this error
            # raise e
            return ImpactLLMResponse(
                **{"drought": None, **{i["tag"]: None for i in self.impact_config}}
            )

        except OutputParserException as e:
            logging.error("OutputParserException: Failed to parse response: %s", e)
            # TODO Handle this error
            # raise e
            return ImpactLLMResponse(
                **{"drought": None, **{i["tag"]: None for i in self.impact_config}}
            )
