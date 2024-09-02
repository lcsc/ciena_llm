import logging
import os
import tempfile
import yaml

from ciena_llm import ClimateImpactExtractor

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


TEST_NAME = "noticias-elpais-sample-194-anotado-e2e"
DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{TEST_NAME}/sample"
RESULTS_DIR = f"./results/{TEST_NAME}/"
os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)

override_config = {"llm": {"model": "llama3:70b"}}
# override_config = {}
with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp_config_file:
    override_config_path = temp_config_file.name
    yaml_str = yaml.dump(override_config, default_flow_style=False, allow_unicode=True)
    temp_config_file.write(yaml_str.encode("utf-8"))

extractor = ClimateImpactExtractor(override_config_path=override_config_path)

articles = extractor(
    dataset_path=DATASET_PATH,
)

extractor.write_excluded_problematic_articles_to_csv(file=f"{RESULTS_DIR}/excluded.csv")

extractor.write_summary_to_csv(
    articles,
    f"{RESULTS_DIR}/summary.csv",
)
