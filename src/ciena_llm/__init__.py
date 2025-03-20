import os
from typing import List, Dict
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
from ciena_llm.extraction_schema.factory import ExtractionSchemaFactory
from ciena_llm.output import OutputManager


class ClimateImpactExtractor:
    def __init__(self, override_config_path=None):
        # Create loaders
        self.article_loader = ArticleLoader()
        self.articles = []  # Empty until __call__
        self.config_loader = ConfigLoader(
            config_path=os.path.join(os.path.dirname(__file__), "config/config.yaml"),
            override_config_path=override_config_path,
        )

        # Create output manager
        self.output_manager = OutputManager(extractor=self)

        # Load configuration
        self.config = self.config_loader.config
        self.stages = self.config.get("stages", {})

        # Define available schemas for extraction stages
        self.extraction_schemas_by_stage = {
            # "event_identification": EventLLMResponse, # TODO not implemented
            "impact_extraction": ExtractionSchemaFactory.get_extraction_schema(
                stage="impact_extraction", config=self.config
            ),
            "location_extraction": ExtractionSchemaFactory.get_extraction_schema(
                stage="location_extraction", config=self.config
            ),
        }

        # Dynamically initialize (enabled) pipeline steps for each stage
        # TODO change name?
        self.enabled_pipeline_steps = {}

        # TODO make dynamic for every step of a stage
        for stage, settings in self.stages.items():
            if settings.get("enable", False):
                schema = self.extraction_schemas_by_stage.get(stage)
                steps = settings.get("steps", {})
                self.enabled_pipeline_steps[stage] = {
                    "extraction": (
                        ExtractionChain(
                            stage=stage,
                            config=steps.get("extraction", {}),
                            llm_config=self.config.get("llm"),
                            extraction_schema=schema,
                            event_config=self.config.get("event"),
                            impact_config=self.config.get("impacts"),
                            response_parsing_enable=(
                                steps.get("response_parsing", {}).get("enable", False)
                            ),
                        )
                        if steps.get("extraction", {}).get("enable", False)
                        else None
                    ),
                    "response_parsing": (
                        ResponseParsingChain(
                            stage=stage,
                            config=steps.get("response_parsing", {}),
                            llm_config=self.config.get("llm"),
                            extraction_schema=schema,
                            event_config=self.config.get("event"),
                            impact_config=self.config.get("impacts"),
                        )
                        if steps.get("response_parsing", {}).get("enable", False)
                        else None
                    ),
                    "summarization": (
                        SummarizationChain(
                            stage=stage,
                            config=steps.get("summarization", {}),
                            llm_config=self.config.get("llm"),
                        )
                        if steps.get("summarization", {}).get("enable", False)
                        else None
                    ),
                }

    def __call__(self, dataset_path: str) -> List[Article]:
        # Load articles
        self.articles = self.article_loader(dataset_path)

        # Process each article
        for article in tqdm(self.articles, desc="Processing articles"):
            logging.debug("START - Processing article: %s", article.filename)

            # Extract article ID and text
            article_id = article.filename  # TODO Or use a unique ID if available
            article_text = article.get_headline_and_body(separator=".")

            # Structure to store extracted data
            extracted_data: Dict[str, dict] = {}

            # Iterate through each stage
            for stage, steps in self.enabled_pipeline_steps.items():
                # Initialize input data for the current stage
                input_data = {
                    "article_id": article_id,
                    "text": article_text,
                }

                # For the current stage, get the pipeline steps
                summarization_chain = steps.get("summarization")
                extraction_chain = steps.get("extraction")
                response_parsing_chain = steps.get("response_parsing")

                # Summarization step (if enabled, will only execute in the first stage)
                if summarization_chain:
                    result = summarization_chain.invoke(input_data)
                    article_text = result["output"]

                # Extraction step (if enabled)
                if extraction_chain:
                    result = extraction_chain.invoke(input_data)
                    input_data["text"] = result["output"]
                    extracted_data[stage] = result["output"]

                # Response Parsing step (if enabled)
                if response_parsing_chain:
                    result = response_parsing_chain.invoke(input_data)
                    extracted_data[stage] = result["output"]

                # Store extracted data in the article
                self._store_extracted_data(
                    article, stage, extracted_data.get(stage, {})
                )

                # If no event is detected, skip dependent stages
                if stage == "event_identification" and not article.drought:
                    logging.debug(
                        "No drought detected in %s, skipping further processing.",
                        article.filename,
                    )
                    break

                # If no impacts are detected, skip dependent stages
                if stage == "impact_extraction" and not article.impacts_aggregated:
                    logging.debug(
                        "No impacts detected in %s, skipping further processing.",
                        article.filename,
                    )
                    break

            # Logging results
            self._log_results(article, extracted_data)

        return self.articles

    def _store_extracted_data(self, article: Article, stage: str, data: dict):
        """Stores extracted data in the article object based on the processing stage."""
        if stage == "event_identification":
            # TODO not implemented
            # article.identified_events = data
            pass
        elif stage == "impact_extraction":
            # TODO would this be in "event_identification"?
            article.drought = data.drought
            # TODO make this extraction better
            article.impacts_aggregated = [
                i for i, v in data.model_dump().items() if v and i != "drought"
            ]
        elif stage == "location_extraction":
            article.provinces = data.response

    def _log_results(self, article: Article, extracted_data: Dict[str, dict]):
        """Logs extracted information for debugging."""
        log_message = f"END - Processed article: {article.filename}\n"

        if "event_identification" in extracted_data:
            # TODO not implemented
            # log_message += (
            #     f"Identified Events: {', '.join(article.identified_events)}\n"
            # )
            pass
        if "impact_extraction" in extracted_data:
            # TODO parametrize for event, now only "drought"
            log_message += f"Drought: {article.drought}\nImpacts: {', '.join(article.impacts_aggregated)}\n"
        if "location_extraction" in extracted_data:
            log_message += f"Provinces: {', '.join(article.provinces)}"

        logging.debug(log_message)
