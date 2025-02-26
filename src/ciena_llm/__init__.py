import os
from typing import List
from tqdm import tqdm
import logging

import dotenv

# pylint: disable=wrong-import-position
dotenv.load_dotenv()

from seqia.article import Article
from seqia.article.loader import ArticleLoader
from seqia.config.loader import ConfigLoader

from ciena_llm.chain import (
    ExtractionChain,
    SummarizationChain,
    ResponseParsingChain,
)
from ciena_llm.response import ProvinceLLMResponse, ImpactLLMResponse
from ciena_llm.output import OutputManager


class ClimateImpactExtractor:
    def __init__(self, override_config_path=None):
        self.article_loader = ArticleLoader()

        self.config_loader = ConfigLoader(
            config_path=os.path.join(os.path.dirname(__file__), "config/config.yaml"),
            override_config_path=override_config_path,
        )

        self.config = self.config_loader.config

        self.task = self.config["task"]

        match self.task:
            case "impact":
                self.extraction_schema = ImpactLLMResponse
            case "province":
                self.extraction_schema = ProvinceLLMResponse
            case _:
                raise ValueError(f"Invalid task in configuration: {self.task}")

        self.extraction_chain = ExtractionChain(
            config=self.config, extraction_schema=self.extraction_schema
        )

        self.summarization_enable = self.config["pipeline"]["summarization"]["enable"]
        self.summarization_chain = SummarizationChain(config=self.config)

        self.response_parsing_enable = self.config["pipeline"]["response_parsing"][
            "enable"
        ]
        self.response_parsing_chain = ResponseParsingChain(
            config=self.config, extraction_schema=self.extraction_schema
        )

        self.output_manager = OutputManager(extractor=self)

    def __call__(self, dataset_path: str) -> List[Article]:
        articles = self.article_loader(dataset_path)

        for article in tqdm(
            articles,
            desc="Summarizing and extracting impacts and locations from articles",
        ):
            article_id = article.filename  # Or use a unique ID if available
            text = article.get_headline_and_body(separator=".")

            input_data = {
                "article_id": article_id,
                "text": text,
            }

            # Run summarization
            if self.summarization_enable:
                result = self.summarization_chain.invoke(input_data)
                input_data["text"] = result["output"]

            # Run extraction
            result = self.extraction_chain.invoke(input_data)
            input_data["text"] = result["output"]
            extracted_data = result["output"]

            # Run response parsing if enabled
            if self.response_parsing_enable:
                result = self.response_parsing_chain.invoke(input_data)
                extracted_data = result["output"]

            # TODO maybe get the article from the chain or make a separate chain component to extract into article
            match self.task:
                case "impact":
                    article.drought = extracted_data.drought
                    article.impacts_aggregated = [
                        i
                        for i, v in extracted_data.model_dump().items()
                        if v and i != "drought"
                    ]

                    logging.debug(
                        f"Article: {article.filename}\n"
                        f"Drought: {article.drought}\n"
                        f"Impacts: {', '.join(article.impacts_aggregated)}"
                    )

                case "province":
                    article.provinces = extracted_data.response

                    logging.debug(
                        f"Article: {article.filename}\n"
                        f"Provinces: {', '.join(article.provinces)}"
                    )

        return articles
