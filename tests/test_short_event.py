from common import ClimateImpactExtractorTest


TEST_NAME = "test_short_event"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-2T-1F/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "gemma3:4b"
STRUCTURED_OUTPUT_MODE = "prompt"

OVERRIDE_CONFIG = {
    "extraction_task": "event",
    "llm": {
        "name": MODEL,
        "structured_output_mode": STRUCTURED_OUTPUT_MODE,
    },
    "steps": {
        "summarization": {
            "enable": True,
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
        "tag": "drought",
        "text_en": "drought",
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
