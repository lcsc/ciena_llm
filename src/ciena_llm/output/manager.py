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
    def stages(self):
        """Get the stages used by the extractor."""
        return self.extractor.stages

    @property
    def pipeline(self):
        """Get the pipeline used by the extractor."""
        return self.extractor.pipeline

    @property
    def enabled_pipeline_steps(self):
        """Get the pipeline steps used by the extractor."""
        return self.extractor.enabled_pipeline_steps

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

        for stage, steps in self.enabled_pipeline_steps.items():
            prompts[stage] = {}
            for step, step_chain in steps.items():
                if step_chain:
                    prompts[stage][step] = step_chain.prompts

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
        for stage, steps in self.enabled_pipeline_steps.items():
            parsing_errors[stage] = {}
            for step, step_chain in steps.items():
                if step_chain and hasattr(step_chain, "parsing_errors"):
                    step_errors = step_chain.parsing_errors
                    parsing_errors[stage][step] = {
                        "parsing_errors": step_errors,
                        "total": len(step_errors),
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
        for stage, steps in self.enabled_pipeline_steps.items():
            stage_total = 0
            execution_times[stage] = {"total": 0}

            for step, step_chain in steps.items():
                if step_chain:
                    step_times = step_chain.execution_times
                    step_total = sum(step_times.values())

                    execution_times[stage][step] = {
                        "total": step_total,
                        "execution_times": step_times,
                    }

                    stage_total += step_total

            execution_times[stage]["total"] = stage_total
            execution_times["total"] += stage_total

        with open(file, "w", encoding="utf-8") as f:
            json.dump(execution_times, f, indent=4)

        return execution_times
