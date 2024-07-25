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
from seqia_gen.prompt import prompt
from seqia_gen.config.loader import ConfigLoader


class ClimateImpactExtractor:
    def __init__(self, model_name: str = "llama3"):

        self.config = ConfigLoader().config
        self.article_loader = ArticleLoader()

        # Initialize the Ollama model
        self.llm = Ollama(model=model_name)

        # Create the LangChain with the LLM and the prompt template
        self.chain = prompt | self.llm

        # Load impacts from configuration
        self.impacts = self.config["impacts"]
        self.impacts_tags = {impact["text"]: impact["tag"] for impact in self.impacts}

    def __call__(self, dataset_path: str) -> List[Article]:
        articles = self.article_loader(dataset_path)

        for article in tqdm(articles, desc="Extracting impacts from articles"):

            article = self.extract(article)

            if article:
                logging.debug(f"Article {article.filename}:\n{article}")

        return articles

    def extract(self, article: Article) -> Optional[Article]:
        text = article.get_headline_and_body(separator=".")
        impacts_text = [impact["text"] for impact in self.impacts]
        response = self.chain.invoke({"text": text, "impacts": impacts_text})
        article, parsed = parse_response_json(article, response, self.impacts_tags)

        if parsed:
            return article

    def write_excluded_problematic_articles_to_csv(self, file: str):
        self.article_loader.write_excluded_problematic_articles_to_csv(file)

    def write_summary_to_csv(self, articles: List[Article], file: str):
        write_summary_to_csv(articles, file, self.config["output"]["summary"])
