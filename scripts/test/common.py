import logging
import os
import tempfile

import yaml

from ciena_llm import ClimateImpactExtractor


def setup_logging(logging_file: str):
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the root logger to the lowest level

    # Create handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Set the stream handler to INFO level

    file_handler = logging.FileHandler(logging_file, mode="w")
    file_handler.setLevel(logging.DEBUG)  # Set the file handler to DEBUG level

    # Create formatters and add them to the handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # Set specific loggers to WARNING level
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Uncomment if needed
    # set_verbose(True)
    # set_debug(True)


class ClimateImpactExtractorTest:
    def __init__(self, test_name, dataset_dir, dataset_path, override_config=None):
        self.test_name = test_name
        self.dataset_dir = dataset_dir
        self.dataset_path = dataset_path
        self.override_config = override_config
        self.results_dir = f"./results/{self.test_name}/"
        os.makedirs(os.path.dirname(self.results_dir), exist_ok=True)
        setup_logging(f"{self.results_dir}/execution.log")

    def run(self):
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
