from common import ClimateImpactExtractorTest


TEST_NAME = "news-elpais-focused-20-8b-provinces"
DATASET_DIR = "news-elpais-focused"
DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/sample_20"
OVERRIDE_CONFIG = {
    "llm": {
        "default": {
            "name": "llama3.1:8b",
        },
    },
    "prompt": {"location_extraction": "location_provinces_extraction_en"},
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_DIR, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
