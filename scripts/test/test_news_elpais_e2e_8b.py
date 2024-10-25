from common import ClimateImpactExtractorTest

TEST_NAME = "news-elpais-e2e-8b"
DATASET_DIR = "news-elpais-sample-194-annotated-e2e"
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
