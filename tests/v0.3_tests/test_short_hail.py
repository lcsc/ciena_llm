from common import ClimateImpactExtractorTest


TEST_NAME = "test_short_hail"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/test-hail-10/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "qwen3:8b"
STRUCTURED_OUTPUT_MODE = "tool"

OVERRIDE_CONFIG = {
    "llm": {
        "name": MODEL,
        "structured_output_mode": STRUCTURED_OUTPUT_MODE,
    },
    "stages": {
        "summarization": {
            "enable": False,
            "steps": {
                "summarization": {
                    "enable": False,
                    "prompt": {"language": LANGUAGE},
                },
            },
        },
        "event_identification": {"enable": False},
        "impact_extraction": {"enable": False},
        "location_extraction": {"enable": False},
        "hail_extraction": {
            "enable": True,
            "steps": {
                "extraction": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
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
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
