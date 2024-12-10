from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation

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
    TEST_NAME = f"news-elpais-e2e-impacts/{MODEL_TEST_NAME}"
    # TEST_NAME = f"news-elpais-e2e-impacts-spanish/{MODEL_TEST_NAME}"
    DATASET_DIR = "news-elpais-sample-194-annotated-e2e"
    DATASET_BASE_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/"
    DATASET_PATH = f"{DATASET_BASE_PATH}/sample-pred-drought/"
    ANNOTATION_PATH = f"{DATASET_BASE_PATH}/dataset.csv"
    OVERRIDE_CONFIG = {
        "pipeline": {
            "drought": {
                "enable": False,
                "exclude": False,
            },
            "impact": {
                "enable": True,
            },
            "location": {
                "enable": False,
            },
            "province": {
                "enable": False,
            },
        },
        "llm": {
            "default": {
                "name": model,
            },
        },
        "prompt": {
            "impact_extraction": "impact_extraction_parser_description_en",
            # "impact_extraction": "impact_extraction_parser_description_es",
            # TODO change source code to use the correct language
            "impact_response_parser": None,
        },
    }

    test = ClimateImpactExtractorTest(
        TEST_NAME, DATASET_DIR, DATASET_PATH, OVERRIDE_CONFIG
    )
    test.run()

    evaluation = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "impact")
    evaluation.run()
