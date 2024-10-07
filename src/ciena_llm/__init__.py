import logging
import os
from typing import List
from tqdm import tqdm

import dotenv

# pylint: disable=wrong-import-position
dotenv.load_dotenv()

from seqia.article import Article
from seqia.article.loader import ArticleLoader
from seqia.config.loader import ConfigLoader
from seqia.utils.output import write_to_csv

from ciena_llm.extractor.drought import DroughtExtractor
from ciena_llm.extractor.impact import ImpactExtractor
from ciena_llm.extractor.location import LocationExtractor


class ClimateImpactExtractor:
    def __init__(self, override_config_path=None):
        self.config_loader = ConfigLoader(
            config_path=os.path.join(os.path.dirname(__file__), "config/config.yaml"),
            override_config_path=override_config_path,
        )
        self.config = self.config_loader.config
        self.pipeline = self.config_loader.get_ordered_pipeline()
        self.pipeline_stages = [stage for stage, _ in self.pipeline]

        logging.info(f"Pipeline: {self.pipeline_stages}")

        self.article_loader = ArticleLoader()

        # TODO pass only extractor specific config
        if "drought" in self.pipeline_stages:
            self.drought_extractor = DroughtExtractor(self.config)
        if "impact" in self.pipeline_stages:
            self.impact_extractor = ImpactExtractor(self.config)
        if "location" in self.pipeline_stages:
            self.location_extractor = LocationExtractor(self.config)

    def __call__(self, dataset_path: str) -> List[Article]:
        articles = self.article_loader(dataset_path)

        for article in tqdm(
            articles, desc="Extracting impacts and locations from articles"
        ):

            for stage, stage_config in self.pipeline:
                match stage:
                    case "drought":
                        article = self.drought_extractor.extract_drought(article)
                        if stage_config["exclude"]:
                            if not article.drought:
                                continue
                    case "impact":
                        # TODO for impact in impacts ?
                        # TODO pass impact name to extractor and to prompt template
                        article = self.impact_extractor.extract_impact(article)
                    case "location":
                        article = self.location_extractor.extract_locations(article)

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
