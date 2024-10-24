from common import ClimateImpactExtractorTest

TEST_NAME = "news-elpais-e2e-70b"
DATASET_DIR = "noticias-elpais-sample-194-anotado-e2e"
DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/sample/"
OVERRIDE_CONFIG = {
    "llm": {
        "default": {
            "name": "llama3.1:70b",
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
