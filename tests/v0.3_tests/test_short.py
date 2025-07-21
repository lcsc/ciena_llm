from common import ClimateImpactExtractorTest


TEST_NAME = "test_short"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-2T-1F/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
# MODEL = "gemma3:4b-it-q4_K_M"
MODEL = "llama3.1:8b"

OVERRIDE_CONFIG = {
    "llm": {
        "name": MODEL,
        "structured_output_mode": "prompt",
    },
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
            "steps": {
                "extraction": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
                        "step": "extraction",
                        "cot": False,
                    },
                },
                "self_criticism": {
                    "enable": False,
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
        "impact_extraction": {
            "enable": True,
            "steps": {
                "extraction": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
                        "step": "extraction",
                        "category": "description",
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
                    },
                },
            },
        },
        "location_extraction": {
            "enable": False,
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
                    "enable": False,
                    "prompt": {
                        "language": LANGUAGE,
                    },
                },
                "response_parsing": {
                    "enable": True,
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
