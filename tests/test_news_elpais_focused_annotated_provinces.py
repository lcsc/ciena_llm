from common import ClimateImpactExtractorTest

MODELS = [
    # "llama3.1:8b",
    # # "llama3.1:70b",
    # "llama3.2:3b",
    # "mistral-small:22b",
    # "gemma2:9b",
    # "gemma2:27b",
    # "qwen2.5:32b",
    "qwq:32b",
]

for model in MODELS:
    MODEL_TEST_NAME = model.replace(":", "-").replace(".", "-")
    TEST_NAME = f"news-elpais-focused-annotated-provinces/{MODEL_TEST_NAME}"
    DATASET_DIR = "news-elpais-focused-annotated-provinces"
    DATASET_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/sample"
    OVERRIDE_CONFIG = {
        "pipeline": {
            "drought": {
                "enable": False,
            },
            "impact": {
                "enable": False,
            },
            "location": {
                "enable": False,
            },
            "province": {  # Only province extraction
                "enable": True,
            },
        },
        "llm": {
            "default": {
                "name": model,
            },
        },
        "prompt": {
            "province_extraction": "provinces_extraction_parser_en",
            "province_response_parser": None,
        },
    }

    test = ClimateImpactExtractorTest(
        TEST_NAME, DATASET_DIR, DATASET_PATH, OVERRIDE_CONFIG
    )
    test.run()
