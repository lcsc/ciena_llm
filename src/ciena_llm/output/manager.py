import json
from typing import List, Dict

from ciena_llm.article import Article
from ciena_llm.output.utils import write_to_csv


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
    def article_loader(self):
        """Get the article loader used by the extractor."""
        return self.extractor.article_loader

    @property
    def articles(self):
        """Get the articles extracted by the extractor."""
        return self.extractor.articles

    @property
    def config_loader(self):
        """Get the configuration loader used by the extractor."""
        return self.extractor.config_loader

    @property
    def config(self):
        """Get the configuration used by the extractor."""
        return self.extractor.config

    @property
    def steps(self):
        """Get the pipeline steps used by the extractor."""
        return self.extractor.steps

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

        for step, step_chain in self.steps.items():
            if step_chain:
                prompts[step] = step_chain.prompts

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
        }

        # Parsing errors from pipeline steps
        for step, step_chain in self.steps.items():
            if step_chain and hasattr(step_chain, "parsing_errors"):
                step_errors = step_chain.parsing_errors
                parsing_errors[step] = {
                    "total": len(step_errors),
                    "parsing_errors": step_errors,
                }
                parsing_errors["total"] += len(step_errors)

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
        }

        # Execution times from pipeline steps

        for step, step_chain in self.steps.items():
            if step_chain:
                step_times = step_chain.execution_times
                step_total = sum(step_times.values())

                execution_times[step] = {
                    "total": step_total,
                    "execution_times": step_times,
                }

                execution_times["total"] += step_total

        with open(file, "w", encoding="utf-8") as f:
            json.dump(execution_times, f, indent=4)

        return execution_times
