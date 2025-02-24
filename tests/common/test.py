import json
import logging
import os
import tempfile
import time
from datetime import datetime

import yaml
from ciena_llm import ClimateImpactExtractor

from .log import setup_logging, format_execution_time


class ClimateImpactExtractorTest:
    def __init__(self, test_name, dataset_path, override_config=None):
        self.test_name = test_name
        self.dataset_path = dataset_path
        self.override_config = override_config
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # TODO make sure results directory is always the same independently of where the script is run from
        base_results_dir = os.path.abspath("./results")
        self.results_dir = os.path.join(base_results_dir, self.test_name, current_time)
        self.latest_results_dir = os.path.join(
            base_results_dir, self.test_name, "latest"
        )
        os.makedirs(self.results_dir, exist_ok=True)
        setup_logging(os.path.join(self.results_dir, "execution.log"))

    def run(self):
        logging.info("Running test %s", self.test_name)

        if self.override_config:
            with tempfile.NamedTemporaryFile(
                suffix=".yaml", delete=False
            ) as temp_config_file:
                override_config_path = temp_config_file.name
                yaml_str = yaml.dump(
                    self.override_config, default_flow_style=False, allow_unicode=True
                )
                temp_config_file.write(yaml_str.encode("utf-8"))
        else:
            override_config_path = None

        extractor = ClimateImpactExtractor(override_config_path)

        start_time = time.time()

        articles = extractor(dataset_path=self.dataset_path)

        execution_time = time.time() - start_time

        # Save results
        extractor.write_summary_to_csv(
            articles, os.path.join(self.results_dir, "summary.csv")
        )
        extractor.write_location_to_csv(
            articles, os.path.join(self.results_dir, "locations.csv")
        )
        extractor.write_config(os.path.join(self.results_dir, "config.yaml"))
        extractor.write_prompts_to_json(os.path.join(self.results_dir, "prompts.json"))
        extractor.write_excluded_problematic_articles_to_csv(
            os.path.join(self.results_dir, "excluded_problematic_articles.csv")
        )
        parsing_errors = extractor.write_parsing_errors_to_json(
            os.path.join(self.results_dir, "parsing_errors.json")
        )
        total_parsing_errors = parsing_errors["total"]

        execution_times = extractor.write_execution_times_to_json(
            os.path.join(self.results_dir, "execution_times.json")
        )
        total_execution_time = format_execution_time(execution_times["total"])

        if os.path.islink(self.latest_results_dir) or os.path.exists(
            self.latest_results_dir
        ):
            os.remove(self.latest_results_dir)
        os.symlink(self.results_dir, self.latest_results_dir)

        logging.info(
            """
--------------------------------
Test %s finished
Results saved in %s
Execution time: %s
Errors: %s
--------------------------------
""",
            self.test_name,
            self.results_dir,
            total_execution_time,
            total_parsing_errors,
        )
