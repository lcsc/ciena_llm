from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import JsonOutputParser

from ciena_llm.llm import LLM
from ciena_llm.prompt.prompt_template_manager import PromptTemplateManager
from ciena_llm.response.impact import ImpactLLMResponse
from ciena_llm.chain.common import invoke_chain


class ImpactExtractionChain(Runnable):
    def __init__(self, config):
        self.step = "extraction"
        self.config = config

        self.task = self.config["task"]  # "impact"

        # TODO parametrize impacts?
        # TODO for impacts only?
        self.impact_config = self.config["impacts"]
        self.pipeline_config = self.config["pipeline"][self.step]

        self.language = self.pipeline_config["prompt"]["language"]

        # If the response parsing pipeline step is disabled in the config, the extraction chain will have to parse the response
        self.response_parsing = not (
            self.config["pipeline"]["response_parsing"]["enable"]
        )

        # TODO get this in prompt template manager?
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

        # TODO do better?
        if self.response_parsing:
            self.response_parser = JsonOutputParser(pydantic_object=ImpactLLMResponse)

            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task=self.task,
                step="multi_classification",
                category="description",
                language=self.language,
                output="json",
                # TODO which one is better?
                # format_instructions=self.response_parser.get_format_instructions(),
                format_instructions=ImpactLLMResponse.get_format_instructions(),
            )

            self.chain = self.prompt_template | self.llm | self.response_parser

        else:
            self.prompt_template = PromptTemplateManager.get_prompt_template(
                task=self.task,
                step="multi_classification",
                category="description",
                language=self.language,
                output="text",
            )

            self.chain = self.prompt_template | self.llm

        self.prompts = {
            "extraction_impact": {
                "task": self.task,
                "step": "multi_classification",
                "category": "description",
                "language": self.language,
                "output": "json" if self.response_parsing else "text",
                "template": self.prompt_template.pretty_repr(),
            },
        }

    def invoke(self, input: str, *args, **kwargs):

        response = invoke_chain(
            self.chain,
            input,
            ImpactLLMResponse,
            ImpactLLMResponse.get_default_response(),
            response_parsing=self.response_parsing,
            impacts=self.impact_names_text,
            impact_descriptions=self.impact_descriptions_text,
        )

        return response
