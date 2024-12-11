from common import ClimateImpactExtractorTest

TEST_NAME = "news-elpais-binary-50T-50F"
DATASET_DIR = "test-datasets-small/news-elpais-binary-50T-50F"
DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/sample"
OVERRIDE_CONFIG = {
    "llm": {
        "name": "llama3.1:70b",
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
