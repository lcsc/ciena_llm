from typing import Optional

from seqia.article import Article

from ciena_llm.llm import LLM
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response import parse_response_bool


class ImpactExtractor:
    def __init__(self, config):
        self.ptm = PromptTemplateManager()

        self.drought_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["drought"]
        )
        self.impact_prompt_template = self.ptm.get_prompt_template(
            config["prompt"]["impact"]
        )

        self.impacts = config["impacts"]

        # Create LLMs for drought and impact stages
        self.drought_llm = LLM(config=config["llm"], stage="drought")
        self.impact_llm = LLM(config=config["llm"], stage="impact")

    def extract_impacts(self, article: Article) -> Optional[Article]:
        text = article.get_headline_and_body(separator=".")

        # DEBUG keep?
        # Check context length for drought prompt
        self.drought_llm.check_context_length(text, self.drought_prompt_template)

        drought_chain = self.drought_prompt_template | self.drought_llm
        drought_response = drought_chain.invoke({"text": text})
        drought_response = parse_response_bool(drought_response)

        article.drought = drought_response

        if not drought_response:
            return article  # TODO what to return?

        for impact in self.impacts:
            impact_chain = self.impact_prompt_template | self.impact_llm
            impact_response = impact_chain.invoke(
                {"text": text, "impact": impact["text"]}
            )
            impact_response = parse_response_bool(impact_response)

            if impact_response:
                article.impacts_aggregated.append(impact["tag"])

        return article
