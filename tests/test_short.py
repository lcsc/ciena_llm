from common import ClimateImpactExtractorTest


BASE_TEST_NAME = "test_short"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-2T-1F/"
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
            "enable": True,
            "prompt": {
                "language": LANGUAGE,
            },
        },
        "response_parsing": {
            "enable": True,
            "prompt": {
                "language": LANGUAGE,
            },
        },
    },
    "llm": {
        "default": {"name": MODEL},
    },
}

impact_override_config = OVERRIDE_CONFIG.copy()
impact_override_config["task"] = "impact"
impact_override_config["pipeline"]["extraction"]["prompt"][
    "category"
] = "multi_classification"
impact_override_config["pipeline"]["extraction"]["prompt"][
    "subcategory"
] = "description"
TEST_NAME = f"{BASE_TEST_NAME}/impact"

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, impact_override_config)
test.run()


province_override_config = OVERRIDE_CONFIG.copy()
province_override_config["task"] = "province"
province_override_config["pipeline"]["extraction"]["prompt"]["category"] = "extraction"
impact_override_config["pipeline"]["extraction"]["prompt"]["subcategory"] = None
TEST_NAME = f"{BASE_TEST_NAME}/province"

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, province_override_config)
test.run()
