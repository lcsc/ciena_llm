from common import ClimateImpactExtractorTest


TEST_NAME = "test_short"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-2T-1F/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "llama3.2:3b"
# MODEL = "llama3.1:8b"

MODELS = [
    "llama3.2:3b-instruct-q4_K_M",
    # "llama3.1:8b-instruct-q4_K_M",
    # "llama3.1:8b-instruct-fp16",
    # "llama3.3:70b-instruct-q4_K_M",
    "gemma2:2b-instruct-q4_K_M",
    # "gemma2:9b-instruct-q4_K_M",
    # "gemma2:9b-instruct-fp16",
    # "gemma2:27b-instruct-q4_K_M",
    "qwen2.5:3b-instruct-q4_K_M",
    # "qwen2.5:7b-instruct-q4_K_M",
    # "qwen2.5:7b-instruct-fp16",
    # "qwen2.5:72b-instruct-q4_K_M",
]

for model in MODELS:

    OVERRIDE_CONFIG = {
        "llm": {"name": model},
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
