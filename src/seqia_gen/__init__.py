import json
import logging
import os
from typing import Optional, List
from tqdm import tqdm

import dotenv

dotenv.load_dotenv()
from langchain_community.llms import Ollama
from seqia.article import Article
from seqia.article.loader import ArticleLoader
from seqia.utils.output import write_summary_to_csv

from seqia_gen.response import parse_response_bool, parse_response_json
from seqia_gen.prompt import get_binary_prompt, get_impact_prompt
from seqia_gen.config.loader import ConfigLoader


class ClimateImpactExtractor:
    def __init__(self, override_config_path=None):
        self.config = ConfigLoader(override_config_path=override_config_path).config

        self.article_loader = ArticleLoader()

        # Initialize the Ollama model
        self.llm_model = self.config["llm"]["model"]
        self.llm_temperature = self.config["llm"]["temperature"]
        self.llm = Ollama(model=self.llm_model, temperature=self.llm_temperature)

        # Load impacts from configuration
        self.impacts = self.config["impacts"]

    def __call__(self, dataset_path: str) -> List[Article]:
        articles = self.article_loader(dataset_path)

        for article in tqdm(articles, desc="Extracting impacts from articles"):

            article = self.extract(article)

            if article:
                logging.debug(f"Article {article.filename}:\n{article}")

        return articles

    def extract(self, article: Article) -> Optional[Article]:
        text = article.get_headline_and_body(separator=".")

        binary_prompt = get_binary_prompt()
        binary_chain = binary_prompt | self.llm
        binary_response = binary_chain.invoke({"text": text})
        binary_response = parse_response_bool(binary_response)

        article.drought = binary_response

        if not binary_response:
            return

        for impact in self.impacts:
            impact_prompt = get_impact_prompt(impact["text"])
            impact_chain = impact_prompt | self.llm
            impact_response = impact_chain.invoke({"text": text})
            impact_response = parse_response_bool(impact_response)

            if impact_response:
                article.impacts_aggregated.append(impact["tag"])

        return article

    def write_excluded_problematic_articles_to_csv(self, file: str):
        self.article_loader.write_excluded_problematic_articles_to_csv(file)

    def write_summary_to_csv(self, articles: List[Article], file: str):
        write_summary_to_csv(articles, file, self.config["output"]["summary"])
