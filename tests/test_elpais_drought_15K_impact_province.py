from common import ClimateImpactExtractorTest


BASE_TEST_NAME = "test_elpais_drought_15K_impact_province"
DATASET_BASE_PATH = "/home/javier/Developer/SeqIA/data/news-elpais-all-drought-seqia"
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "gemma2:9b"

OVERRIDE_CONFIG = {
    # "task": "impact",
    "pipeline": {
        "extraction": {
            "enable": True,
            "prompt": {
                "language": LANGUAGE,
            },
        },
        "summarization": {
            "enable": False,
            "prompt": {
                "language": LANGUAGE,
            },
        },
        "response_parsing": {
            "enable": False,
            "prompt": {
                "language": LANGUAGE,
            },
        },
    },
    "llm": {
        "default": {"name": MODEL},
    },
}

OVERRIDE_CONFIG["task"] = "impact"
TEST_NAME = f"{BASE_TEST_NAME}/impact"

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()


OVERRIDE_CONFIG["task"] = "province"
TEST_NAME = f"{BASE_TEST_NAME}/province"

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
