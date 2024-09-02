import logging
import os

from ciena_llm import ClimateImpactExtractor

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

TEST_NAME = "news-elpais-binary-50T-50F"
# TEST_NAME = "news-elpais-binary-50T-50F"
DATASET_PATH = (
    f"/home/javier/Developer/SeqIA/data/test-datasets-small/{TEST_NAME}/sample"
)
RESULTS_DIR = f"./results/{TEST_NAME}/"
os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)


extractor = ClimateImpactExtractor()

articles = extractor(
    dataset_path=DATASET_PATH,
)

extractor.write_excluded_problematic_articles_to_csv(file=f"{RESULTS_DIR}/excluded.csv")

extractor.write_summary_to_csv(
    articles,
    f"{RESULTS_DIR}/summary.csv",
)
