from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import JsonOutputParser

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.province import ProvinceLLMResponse
from ciena_llm.chain.common import invoke_chain


class ProvinceExtractionChain(Runnable):
    def __init__(self, config):
        self.step = "extraction"
        self.config = config

        self.task = self.config["task"]  # "province"

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

            # TODO maybe put this in the prompt template manager?
            # JSON format instructions for the model
            format_instructions = """
```json 
{
    "response": [
        "province name 1",
        "province name 2",
    ]
}
```
"""

            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task=self.task,
                step="extraction",
                language=self.language,
                output="json",
                format_instructions=format_instructions,
            )

            def parse_response_to_dict(response):
                """
                Parser to ensure the response is always a dictionary

                Convert the response to a dictionary if it is a list.
                This handles common generation errors in the LLM when no provinces are found.
                """
                if isinstance(response, list):
                    return {"response": response}
                if not isinstance(response, dict):
                    return {"response": []}
                return response

            self.chain = (
                self.prompt_template
                | self.llm
                | self.response_parser
                | parse_response_to_dict
            )

        else:
            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task=self.task,
                step="extraction",
                language=self.language,
                output="text",
            )

            self.chain = self.prompt_template | self.llm

        self.prompts = {
            "extraction_province": {
                "task": self.task,
                "step": "extraction",
                "language": self.language,
                "output": "json" if self.response_parsing else "text",
                "template": self.prompt_template.pretty_repr(),
            },
        }

    def invoke(self, input: str, *args, **kwargs):

        response = invoke_chain(
            self.chain,
            input,
            ProvinceLLMResponse,
            {"response": []},
            response_parsing=self.response_parsing,
        )

        return response
