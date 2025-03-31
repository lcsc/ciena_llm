from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation


TEST_NAME = "test_short_12"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/cesga-test-12/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"
ANNOTATION_PATH = f"{DATASET_BASE_PATH}/dataset.csv"

LANGUAGE = "en"
MODEL = "llama3.2:3b"
# MODEL = "llama3.1:8b"

OVERRIDE_CONFIG = {
    "llm": {"name": MODEL},
    "stages": {
        "summarization": {
            "enable": False,
            "steps": {
                "summarization": {
                    "enable": False,
                    "prompt": {
                        "language": LANGUAGE,
                    },
                },
            },
        },
        "event_identification": {
            "enable": False,
        },
        "impact_extraction": {
            "enable": True,
            "steps": {
                "extraction": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
                        "step": "extraction",
                        "category": "description",
                        "cot": True,
                    },
                },
                "self_criticism": {
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
        },
        "location_extraction": {
            "enable": True,
            "steps": {
                "extraction": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
                        "step": "extraction",
                        "category": "province",
                        "cot": False,
                    },
                },
                "self_criticism": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
                    },
                },
                "response_parsing": {
                    "enable": False,
                    "prompt": {
                        "language": LANGUAGE,
                        "category": "province",
                    },
                },
            },
        },
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()

eval = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "impact")
eval.run()
