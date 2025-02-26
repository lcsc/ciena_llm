import json
from typing import List, Dict

from seqia.article import Article
from seqia.utils.output import write_to_csv


class OutputManager:
    """
    Manager class to handle the output of the ClimateImpactExtractor.

    This class provides methods to write the extracted data to files.

    :param extractor: The ClimateImpactExtractor instance to manage the output of.
    """

    def __init__(self, extractor: "ClimateImpactExtractor"):
        # Store only a reference, not the actual data
        self.extractor = extractor

    # Properties to access the extractor's properties dynamically after initialization

    @property
    def articles(self):
        """Get the articles extracted by the extractor."""
        return self.extractor.articles

    @property
    def article_loader(self):
        """Get the article loader used by the extractor."""
        return self.extractor.article_loader

    @property
    def config(self):
        """Get the configuration used by the extractor."""
        return self.extractor.config

    @property
    def config_loader(self):
        """Get the configuration loader used by the extractor."""
        return self.extractor.config_loader

    @property
    def extraction_chain(self):
        """Get the extraction chain used by the extractor."""
        return self.extractor.extraction_chain

    @property
    def summarization_chain(self):
        """Get the summarization chain used by the extractor."""
        return self.extractor.summarization_chain

    @property
    def response_parsing_chain(self):
        """Get the response parsing chain used by the extractor."""
        return self.extractor.response_parsing_chain

    @property
    def summarization_enable(self):
        """Check if summarization is enabled in the extractor."""
        return self.extractor.summarization_enable

    @property
    def response_parsing_enable(self):
        """Check if response parsing is enabled in the extractor."""
        return self.extractor.response_parsing_enable

    # Methods to write the extracted data to files

    def write_excluded_problematic_articles_to_csv(self, file: str):
        """
        Write the articles that were excluded due to problematic content to the given CSV file.

        :param file: The file to write the excluded articles to.
        """
        self.article_loader.write_excluded_problematic_articles_to_csv(file)

    def write_summary_to_csv(self, articles: List[Article], file: str):
        """
        Write the summary of the extracted data to the given CSV file.

        :param articles: The articles to write the summary of.
        :param file: The file to write the summary to.
        """
        write_to_csv(articles, file, self.config["output"]["summary"], "article")

    def write_location_to_csv(self, articles: List[Article], file: str):
        """
        Write the extracted location data to the given CSV file.

        :param articles: The articles to write the location data of.
        :param file: The file to write the location data to.
        """
        write_to_csv(
            articles,
            file,
            self.config["output"]["location_article"],
            "location_article",
        )

    def write_config(self, file: str):
        """
        Write the configuration used by the extractor to the given YAML file.

        :param file: The file to write the configuration to.
        """
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

    def write_parsing_errors_to_json(self, file: str) -> Dict:
        """
        Write the parsing errors encountered during the extraction process to the given JSON file.

        :param file: The file to write the parsing errors to.
        :return: The parsing errors dictionary.
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
        :return: The execution times dictionary.
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
