import os
import json
from typing import List, Dict
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
from ciena_llm.chain import (
    ExtractionChain,
    SummarizationChain,
    ResponseParsingChain,
)
from ciena_llm.response import ProvinceLLMResponse, ImpactLLMResponse


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

        prompts.update(self.extraction_chain.prompts)

        if self.summarization_enable:
            prompts.update(self.summarization_chain.prompts)

        if self.response_parsing_enable:
            prompts.update(self.response_parsing_chain.prompts)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(prompts, f, indent=4)

    def write_parsing_errors_to_json(self, file: str):
        """
        Write the parsing errors encountered during the extraction process to the given JSON file.

        :param file: The file to write the parsing errors to.
        """

        parsing_errors = {
            "total": 0,
            "extraction": {
                "parsing_errors": {},
                "total": 0,
            },
            "response_parsing": {
                "parsing_errors": {},
                "total": 0,
            },
        }

        # Parsing errors from extraction chain
        parsing_errors["extraction"][
            "parsing_errors"
        ] = self.extraction_chain.parsing_errors
        parsing_errors["extraction"]["total"] = len(
            self.extraction_chain.parsing_errors
        )
        parsing_errors["total"] += len(self.extraction_chain.parsing_errors)

        # Parsing errors from response parsing chain
        if self.response_parsing_enable:
            parsing_errors["response_parsing"][
                "parsing_errors"
            ] = self.response_parsing_chain.parsing_errors
            parsing_errors["response_parsing"]["total"] = len(
                self.response_parsing_chain.parsing_errors
            )
            parsing_errors["total"] += len(self.response_parsing_chain.parsing_errors)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(parsing_errors, f, indent=4)

        return parsing_errors

    def write_execution_times_to_json(self, file: str) -> Dict:
        """
        Write the execution times for the extraction process to the given JSON file.

        :param file: The file to write the execution times to.
        """

        execution_times = {
            "total": 0,
            "summarization": {
                "total": 0,
                "individual": {},
            },
            "extraction": {
                "total": 0,
                "individual": {},
            },
            "response_parsing": {
                "total": 0,
                "individual": {},
            },
        }

        # Execution times from summarization chain
        if self.summarization_enable:
            execution_times["summarization"][
                "individual"
            ] = self.summarization_chain.execution_times
            execution_times["summarization"]["total"] = sum(
                self.summarization_chain.execution_times.values()
            )
            execution_times["total"] += execution_times["summarization"]["total"]

        # Execution times from extraction chain
        execution_times["extraction"][
            "individual"
        ] = self.extraction_chain.execution_times
        execution_times["extraction"]["total"] = sum(
            self.extraction_chain.execution_times.values()
        )
        execution_times["total"] += execution_times["extraction"]["total"]

        # Execution times from response parsing chain
        if self.response_parsing_enable:
            execution_times["response_parsing"][
                "individual"
            ] = self.response_parsing_chain.execution_times
            execution_times["response_parsing"]["total"] = sum(
                self.response_parsing_chain.execution_times.values()
            )
            execution_times["total"] += execution_times["response_parsing"]["total"]

        with open(file, "w", encoding="utf-8") as f:
            json.dump(execution_times, f, indent=4)

        return execution_times
