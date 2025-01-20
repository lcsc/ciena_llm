from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import JsonOutputParser

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.impact import ImpactLLMResponse
from ciena_llm.response.province import ProvinceLLMResponse
from ciena_llm.chain.common import invoke_chain


class ResponseParsingChain(Runnable):
    def __init__(self, config):
        self.step = "response_parsing"
        self.config = config

        self.task = self.config["task"]

        # TODO get this in prompt template manager?
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

        match self.task:
            case "impact":
                self.response_parser = JsonOutputParser(
                    pydantic_object=ImpactLLMResponse
                )
            case "province":
                self.response_parser = JsonOutputParser(
                    pydantic_object=ProvinceLLMResponse
                )

        self.prompt_template = PromptTemplateManager.get_prompt_template(
            task=self.task,
            step=self.step,
            language=self.language,
            output="json",
            format_instructions=self.response_parser.get_format_instructions(),
        )

        self.chain = self.prompt_template | self.llm | self.response_parser

        self.prompts = {
            "extraction_impact": {
                "task": self.task,
                "step": self.step,
                "language": self.language,
                "output": "json",
                "template": self.prompt_template.pretty_repr(),
            },
        }

    def invoke(self, input: str, *args, **kwargs):

        match self.task:
            case "impact":
                return invoke_chain(
                    self.chain,
                    input,
                    ImpactLLMResponse,
                    {"drought": None, **{i["tag"]: None for i in self.impact_config}},
                    impacts=self.impact_names_text,
                    impact_descriptions=self.impact_descriptions_text,
                )
            case "province":
                return invoke_chain(
                    self.chain,
                    input,
                    ProvinceLLMResponse,
                    {"response": []},
                )
