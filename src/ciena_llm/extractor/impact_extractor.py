from typing import Optional

from seqia.article import Article

from ciena_llm.extractor import BaseExtractor
from ciena_llm.prompt_template_manager import PromptTemplateManager
from ciena_llm.response import parse_response_bool


class ImpactExtractor(BaseExtractor):
    def __init__(self, config):
        super().__init__(config)

        self.ptm = PromptTemplateManager()

        self.binary_prompt_template = self.ptm.get_prompt_template(
            self.config["prompt"]["binary"]
        )
        self.impact_prompt_template = self.ptm.get_prompt_template(
            self.config["prompt"]["impact"]
        )

        self.impacts = self.config["impacts"]

    def extract_impacts(self, article: Article) -> Optional[Article]:
        text = article.get_headline_and_body(separator=".")

        self.check_context_length(text, self.binary_prompt_template)

        binary_chain = (
            self.binary_prompt_template
            | (lambda text: self.log("Input to LLM (Binary)", text))
            | self.llm
            | (lambda text: self.log("Output from LLM (Binary)", text))
        )
        binary_response = binary_chain.invoke({"text": text})
        binary_response = parse_response_bool(binary_response)

        article.drought = binary_response

        if not binary_response:
            return

        for impact in self.impacts:
            impact_chain = (
                self.impact_prompt_template
                | (lambda text: self.log("Input to LLM (Impacts)", text))
                | self.llm
                | (lambda text: self.log("Output from LLM (Impacts)", text))
            )
            impact_response = impact_chain.invoke(
                {"text": text, "impact": impact["text"]}
            )
            impact_response = parse_response_bool(impact_response)

            if impact_response:
                article.impacts_aggregated.append(impact["tag"])

        return article
