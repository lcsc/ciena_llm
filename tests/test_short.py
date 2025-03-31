from common import ClimateImpactExtractorTest


TEST_NAME = "test_short"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-2T-1F/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "llama3.2:3b"
# MODEL = "llama3.1:8b"

OVERRIDE_CONFIG = {
    "llm": {"name": MODEL},
    "stages": {
        "summarization": {
            "enable": True,
            "steps": {
                "summarization": {
                    "enable": True,
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
