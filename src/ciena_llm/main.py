import logging
import os

from ciena_llm import ClimateImpactExtractor

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# TODO take this a cli parameters
MODEL_NAME = "llama3"
TEST_NAME = "news-elpais-binary-50T-50F"
DATASET_PATH = (
    f"/home/javier/Developer/SeqIA/data/test-datasets-small/{TEST_NAME}/sample"
)
RESULTS_DIR = f"./results/{TEST_NAME}/"
os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)


def main():
    extractor = ClimateImpactExtractor(model_name=MODEL_NAME)

    articles = extractor(
        dataset_path=DATASET_PATH,
    )

    extractor.write_excluded_problematic_articles_to_csv(
        file=f"{RESULTS_DIR}/excluded.csv"
    )

    extractor.write_summary_to_csv(
        articles,
        f"{RESULTS_DIR}/summary.csv",
    )


if __name__ == "__main__":
    main()
