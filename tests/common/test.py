import os
import tempfile
import time
from datetime import datetime

import yaml
from ciena_llm import ClimateImpactExtractor

from .log import setup_logging, format_execution_time


class ClimateImpactExtractorTest:
    def __init__(self, test_name, dataset_dir, dataset_path, override_config=None):
        self.test_name = test_name
        self.dataset_dir = dataset_dir
        self.dataset_path = dataset_path
        self.override_config = override_config
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # TODO make sure results directory is always the same independently of where the script is run from
        self.results_dir = f"./results/{self.test_name}/{current_time}/"
        os.makedirs(os.path.dirname(self.results_dir), exist_ok=True)
        setup_logging(f"{self.results_dir}/execution.log")

    def run(self):
        start_time = time.time()

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
        articles = extractor(dataset_path=self.dataset_path)
        extractor.write_summary_to_csv(articles, f"{self.results_dir}/summary.csv")
        extractor.write_location_to_csv(articles, f"{self.results_dir}/locations.csv")
        extractor.write_config(f"{self.results_dir}/config.yaml")
        extractor.write_prompts_to_json(f"{self.results_dir}/prompts.json")

        end_time = time.time()
        execution_time = end_time - start_time

        with open(f"{self.results_dir}/execution_time.txt", "w") as time_file:
            time_str = format_execution_time(execution_time)
            time_file.write(time_str)
