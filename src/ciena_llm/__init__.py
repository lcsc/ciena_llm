import os
import json
from typing import List, Dict
from tqdm import tqdm
import logging

import dotenv

# pylint: disable=wrong-import-position
dotenv.load_dotenv()

from ciena_llm.article import Article
from ciena_llm.article.loader import ArticleLoader
from ciena_llm.config.loader import ConfigLoader

from ciena_llm.chain import (
    ExtractionChain,
    SummarizationChain,
    ResponseParsingChain,
    SelfCriticismChain,
)
from ciena_llm.extraction_schema.factory import ExtractionSchemaFactory
from ciena_llm.output import OutputManager


class ClimateImpactExtractor:
    def __init__(self, override_config_path=None):
        # Create loaders
        self.article_loader = ArticleLoader()
        self.articles = []
        self.config_loader = ConfigLoader(
            config_path=os.path.join(os.path.dirname(__file__), "config/config.yaml"),
            override_config_path=override_config_path,
        )

        # Create output manager
        self.output_manager = OutputManager(extractor=self)

        # Load configuration
        self.config = self.config_loader.config
        self.steps_config = self.config.get("steps", {})

        self.extraction_task = self.config.get("extraction_task")
        extraction_schema = ExtractionSchemaFactory.get_extraction_schema(
            name=self.extraction_task, config=self.config
        )

        self.summarization_chain = (
            SummarizationChain(
                config=self.steps_config.get("summarization", {}),
                llm_config=self.config.get("llm"),
            )
            if self.steps_config.get("summarization", {}).get("enable", False)
            else None
        )
        self.extraction_chain = (
            ExtractionChain(
                extraction_task=self.extraction_task,
                config=self.steps_config.get("extraction", {}),
                llm_config=self.config.get("llm"),
                extraction_schema=(
                    extraction_schema
                    if not self.steps_config.get("response_parsing", {}).get(
                        "enable", False
                    )
                    else None
                ),
                event_config=self.config.get("event"),
                impact_config=self.config.get("impacts"),
            )
            if self.steps_config.get("extraction", {}).get("enable", False)
            else None
        )
        self.self_criticism_chain = (
            SelfCriticismChain(
                config=self.steps_config.get("self_criticism", {}),
                llm_config=self.config.get("llm"),
                extraction_schema=(
                    extraction_schema
                    if not self.steps_config.get("response_parsing", {}).get(
                        "enable", False
                    )
                    else None
                ),
            )
            if self.steps_config.get("self_criticism", {}).get("enable", False)
            else None
        )
        self.response_parsing_chain = (
            ResponseParsingChain(
                extraction_task=self.extraction_task,
                config=self.steps_config.get("response_parsing", {}),
                llm_config=self.config.get("llm"),
                extraction_schema=extraction_schema,
                event_config=self.config.get("event"),
                impact_config=self.config.get("impacts"),
            )
            if self.steps_config.get("response_parsing", {}).get("enable", False)
            else None
        )

        self.steps = {
            "summarization": self.summarization_chain,
            "extraction": self.extraction_chain,
            "self_criticism": self.self_criticism_chain,
            "response_parsing": self.response_parsing_chain,
        }

    def __call__(self, dataset_path: str) -> List[Article]:
        # Load articles
        self.articles = self.article_loader(dataset_path)

        # Process each article
        for article in tqdm(self.articles, desc="Processing articles"):
            logging.debug("START - Processing article: %s", article.filename)

            # Extract article ID and text
            article_id = article.filename
            article_text = article.get_headline_and_body_and_date()

            # Structure to store extracted data
            extracted_data = {}

            # Initialize input data
            input_data = {
                "article_id": article_id,
                "text": article_text,
            }

            # Summarization step (if enabled, will only execute in the first stage)
            if self.summarization_chain:
                result = self.summarization_chain.invoke(input_data)
                article_text = result["output"]
                input_data["text"] = article_text

            # Extraction step (if enabled)
            if self.extraction_chain:
                result = self.extraction_chain.invoke(input_data)
                input_data["text"] = result["output"]
                extracted_data = result["output"]

            # Self-Criticism step (if enabled)
            if self.self_criticism_chain:
                self_criticism_input_data = {
                    "article_id": article_id,
                    "prompt": self.extraction_chain.prompt_template.invoke(
                        article_text
                    ).text,
                    "response": (
                        json.dumps(input_data["text"].model_dump())
                        if not self.response_parsing_chain
                        else input_data["text"]
                    ),
                }
                result = self.self_criticism_chain.invoke(self_criticism_input_data)
                extracted_data = result["output"]

            # Response Parsing step (if enabled)
            if self.response_parsing_chain:
                result = self.response_parsing_chain.invoke(input_data)
                extracted_data = result["output"]

            # Store extracted data in the article
            article.extracted_data = (
                extracted_data.model_dump() if extracted_data.model_dump() else {}
            )

            # Logging results
            self._log_results(article)

        return self.articles

    def _log_results(self, article: Article):
        """Logs extracted information for debugging."""
        log_message = f"END - Processed article: {article.filename}\n"

        log_message += (
            f"Extracted Data: {json.dumps(article.extracted_data, indent=2)}\n"
        )

        logging.debug(log_message)
