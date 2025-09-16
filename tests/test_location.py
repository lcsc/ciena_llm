import os

from common import ClimateImpactExtractorTest


TEST_NAME = "test_location"
DATASET_BASE_PATH = os.getenv("DATASET_BASE_PATH")
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "gemma3:4b"
STRUCTURED_OUTPUT_MODE = "prompt"

OVERRIDE_CONFIG = {
    "extraction_task": "location",
    "llm": {
        "name": MODEL,
        "structured_output_mode": STRUCTURED_OUTPUT_MODE,
    },
    "steps": {
        "summarization": {
            "enable": False,
            "prompt": {"language": LANGUAGE},
        },
        "extraction": {
            "enable": True,
            "prompt": {
                "language": LANGUAGE,
                "category": "province",
                "cot": True,
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
    "event": {
        "tag": "drought",
        "text_en": "drought",
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
