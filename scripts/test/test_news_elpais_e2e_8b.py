from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation

TEST_NAME = "news-elpais-e2e-8b"
DATASET_DIR = "news-elpais-sample-194-annotated-e2e"
DATASET_BASE_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/"
DATASET_PATH = f"{DATASET_BASE_PATH}/sample/"
ANNOTATION_PATH = f"{DATASET_BASE_PATH}/dataset.csv"
OVERRIDE_CONFIG = {
    "llm": {
        "default": {
            "name": "llama3.1:8b",
        },
    },
    "pipeline": {
        "drought": {
            "enable": True,
            "exclude": True,
        },
        "impact": {
            "enable": True,
        },
        "location": {
            "enable": True,
        },
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_DIR, DATASET_PATH, OVERRIDE_CONFIG)
test.run()

eval = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "impact")
eval.run()
