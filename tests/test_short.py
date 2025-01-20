from common import ClimateImpactExtractorTest


BASE_TEST_NAME = "test_short"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-5T-2F/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"
ANNOTATION_PATH = f"{DATASET_BASE_PATH}/labels.csv"

LANGUAGE = "es"
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

# OVERRIDE_CONFIG["task"] = "impact"
# TEST_NAME = f"{BASE_TEST_NAME}/impact"

# test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
# test.run()


OVERRIDE_CONFIG["task"] = "province"
TEST_NAME = f"{BASE_TEST_NAME}/province"

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
