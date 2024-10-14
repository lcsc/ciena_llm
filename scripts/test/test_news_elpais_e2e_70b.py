import os
import tempfile

import yaml

from common import setup_logging

from ciena_llm import ClimateImpactExtractor


TEST_NAME = "news-elpais-e2e-70b"
DATASET_DIR = "noticias-elpais-sample-194-anotado-e2e"
DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/sample/"
RESULTS_DIR = f"./results/{TEST_NAME}/"
os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)

setup_logging(f"{RESULTS_DIR}/execution.log")

override_config = {
    "llm": {
        "default": {
            "name": "llama3.1:70b",
        },
    },
}
with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp_config_file:
    override_config_path = temp_config_file.name
    yaml_str = yaml.dump(override_config, default_flow_style=False, allow_unicode=True)
    temp_config_file.write(yaml_str.encode("utf-8"))


extractor = ClimateImpactExtractor(override_config_path)

articles = extractor(
    dataset_path=DATASET_PATH,
)

extractor.write_summary_to_csv(articles, f"{RESULTS_DIR}/summary.csv")

extractor.write_location_to_csv(articles, f"{RESULTS_DIR}/locations.csv")

extractor.write_config(f"{RESULTS_DIR}/config.yaml")
