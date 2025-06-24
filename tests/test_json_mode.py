from common import ClimateImpactExtractorTest  # , ClimateImpactExtractorEvaluation


DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-50T-50F"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"

OVERRIDE_CONFIG = {
    "llm": {
        "name": "llama3.1:8b",
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


# MODEL = "llama3.2:3b"
# OVERRIDE_CONFIG["llm"]["name"] = MODEL
# OVERRIDE_CONFIG["llm"]["structured_output_mode"] = "prompt"
# TEST_NAME = f"test_json_mode/{MODEL}/prompt"
# test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
# test.run()

# MODEL = "llama3.2:3b"
# OVERRIDE_CONFIG["llm"]["name"] = MODEL
# OVERRIDE_CONFIG["llm"]["structured_output_mode"] = "tool"
# TEST_NAME = f"test_json_mode/{MODEL}/tool"
# test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
# test.run()

# TODO fails with an error
# MODEL = "gemma3:4b"
# OVERRIDE_CONFIG["llm"]["name"] = MODEL
# OVERRIDE_CONFIG["llm"]["structured_output_mode"] = "prompt"
# TEST_NAME = f"test_json_mode/{MODEL}/prompt"
# test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
# test.run()

# TODO does not support tool calling
# MODEL = "gemma3:4b"
# OVERRIDE_CONFIG["llm"]["name"] = MODEL
# OVERRIDE_CONFIG["llm"]["structured_output_mode"] = "tool"
# TEST_NAME = f"test_json_mode/{MODEL}/tool"
# test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
# test.run()
