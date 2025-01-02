import os
import json
from typing import List
from tqdm import tqdm
import logging

import dotenv

# pylint: disable=wrong-import-position
dotenv.load_dotenv()

from seqia.article import Article
from seqia.article.loader import ArticleLoader
from seqia.config.loader import ConfigLoader
from seqia.utils.output import write_to_csv

from ciena_llm.llm import LLM
from ciena_llm.chain import ExtractionChain, SummarizationChain, ResponseParsingChain


class ClimateImpactExtractor:
    def __init__(self, override_config_path=None):
        self.article_loader = ArticleLoader()

        self.config_loader = ConfigLoader(
            config_path=os.path.join(os.path.dirname(__file__), "config/config.yaml"),
            override_config_path=override_config_path,
        )

        self.config = self.config_loader.config

        # TODO organize better config
        self.summarization_enable = self.config["pipeline"]["summarization"]["enable"]
        self.response_parsing_enable = self.config["pipeline"]["response_parsing"][
            "enable"
        ]

        self.summarization_chain = SummarizationChain(config=self.config)
        self.extraction_chain = ExtractionChain(config=self.config)
        self.response_parsing_chain = ResponseParsingChain(config=self.config)

        self.chain = self.extraction_chain

        if self.summarization_enable:
            self.chain = self.summarization_chain | self.chain

        if self.response_parsing_enable:
            self.chain = self.chain | self.response_parsing_chain

    def __call__(self, dataset_path: str) -> List[Article]:
        articles = self.article_loader(dataset_path)

        for article in tqdm(
            articles,
            desc="Summarizing and extracting impacts and locations from articles",
        ):
            text = article.get_headline_and_body(separator=".")

            # Run the combined summarization and extraction chain
            output = self.chain.invoke(text)

            article.drought = output.drought
            article.impacts_aggregated = [
                i for i, v in output.model_dump().items() if v and i != "drought"
            ]

            logging.info(
                f"Article {article.filename}\nDrought: {article.drought}\nImpacts: {article.impacts_aggregated}"
            )

        return articles

    def write_excluded_problematic_articles_to_csv(self, file: str):
        self.article_loader.write_excluded_problematic_articles_to_csv(file)

    def write_summary_to_csv(self, articles: List[Article], file: str):
        write_to_csv(articles, file, self.config["output"]["summary"], "article")

    def write_location_to_csv(self, articles: List[Article], file: str):
        write_to_csv(
            articles,
            file,
            self.config["output"]["location_article"],
            "location_article",
        )

    def write_config(self, file: str):
        self.config_loader.save_config(file)

    def write_prompts_to_json(self, file: str):
        """
        Write the prompts used by the extractors to the given JSON file.

        :param file: The file to write the prompts to.
        """
        prompts = {}

        with open(file, "w", encoding="utf-8") as f:
            json.dump(prompts, f, indent=4)
