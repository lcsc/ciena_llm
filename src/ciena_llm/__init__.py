import logging
import os
from typing import List
from tqdm import tqdm

import dotenv
import json

# pylint: disable=wrong-import-position
dotenv.load_dotenv()

from seqia.article import Article
from seqia.article.loader import ArticleLoader
from seqia.config.loader import ConfigLoader
from seqia.utils.output import write_to_csv

from ciena_llm.classifier.drought import DroughtClassifier
from ciena_llm.classifier.impact import ImpactClassifier
from ciena_llm.extractor.location import LocationExtractor
from ciena_llm.extractor.province import ProvinceExtractor


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
            self.drought_classifier = DroughtClassifier(self.config)
        if "impact" in self.pipeline_stages:
            self.impact_classifier = ImpactClassifier(self.config)
        if "location" in self.pipeline_stages:
            self.location_extractor = LocationExtractor(self.config)
        if "province" in self.pipeline_stages:
            self.province_extractor = ProvinceExtractor(self.config)

    def __call__(self, dataset_path: str) -> List[Article]:
        articles = self.article_loader(dataset_path)

        for article in tqdm(
            articles, desc="Extracting impacts and locations from articles"
        ):

            for stage, stage_config in self.pipeline:
                match stage:
                    case "drought":
                        article = self.drought_classifier.classify(article)
                        if stage_config["exclude"]:
                            if not article.drought:
                                continue
                    case "impact":
                        article = self.impact_classifier.classify(article)
                    case "location":
                        article = self.location_extractor.extract_locations(article)
                    case "province":
                        article = self.province_extractor.extract_provinces(article)

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

        if "drought" in self.pipeline_stages:
            prompts.update(self.drought_classifier.prompts)
        if "impact" in self.pipeline_stages:
            prompts.update(self.impact_classifier.prompts)
        if "location" in self.pipeline_stages:
            prompts.update(self.location_extractor.prompts)
        if "province" in self.pipeline_stages:
            prompts.update(self.province_extractor.prompts)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(prompts, f, indent=4)
