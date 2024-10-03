import logging
import os
from typing import Optional, List
from tqdm import tqdm

import dotenv

# pylint: disable=wrong-import-position
dotenv.load_dotenv()
from seqia.article import Article
from seqia.article.loader import ArticleLoader
from seqia.utils.output import write_to_csv
from seqia.config.loader import ConfigLoader

from ciena_llm.extractor.impact_extractor import ImpactExtractor
from ciena_llm.extractor.location_extractor import LocationExtractor


class ClimateImpactExtractor:
    def __init__(self, override_config_path=None):
        self.config_loader = ConfigLoader(
            config_path=os.path.join(os.path.dirname(__file__), "config/config.yaml"),
            override_config_path=override_config_path,
        )
        self.config = self.config_loader.config

        # TODO pass only extractor specific config
        self.impact_extractor = ImpactExtractor(self.config)
        # TODO pass only extractor specific config
        self.location_extractor = LocationExtractor(self.config)

        self.article_loader = ArticleLoader()

    def __call__(self, dataset_path: str) -> List[Article]:
        articles = self.article_loader(dataset_path)

        for article in tqdm(
            articles, desc="Extracting impacts and locations from articles"
        ):

            # TODO read pipeline from config to apply each extractor extractors
            article = self.impact_extractor.extract_impacts(article)
            if not article:
                continue
            article = self.location_extractor.extract_locations(article)

            # DEBUG
            # if article:
            #     logging.debug("Article %s:\n%s", article.filename, article)

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
