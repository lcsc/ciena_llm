from common import ClimateImpactExtractorTest

TEST_NAME = "noticias-elpais-sample-194-anotado-e2e"
DATASET_DIR = "noticias-elpais-sample-194-anotado-e2e"
DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/sample"
OVERRIDE_CONFIG = {
    "llm": {
        "model": "llama3:70b",
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_DIR, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
