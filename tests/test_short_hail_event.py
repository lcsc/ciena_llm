from common import ClimateImpactExtractorTest


TEST_NAME = "test_short_hail_event"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/test-hail-10/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "gemma3:4b"
STRUCTURED_OUTPUT_MODE = "prompt"

OVERRIDE_CONFIG = {
    "extraction_task": "hail_event",
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
            },
        },
    },
    "event": {
        "tag": "hail",
        "text_en": "hail",
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
