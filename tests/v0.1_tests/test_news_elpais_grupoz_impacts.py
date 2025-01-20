from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation

MODELS = [
    "llama3.2:3b",
    "llama3.1:8b",
    # "llama3.1:70b",
    "mistral-small:22b",
    "gemma2:9b",
    "gemma2:27b",
    "qwen2.5:32b",
]

for model in MODELS:
    MODEL_TEST_NAME = model.replace(":", "-").replace(".", "-")
    # TODO change spanish to english another test
    # TODO need to also change the source code to use the correct language
    TEST_NAME = f"news-elpais-grupoz-impacts-spanish/{MODEL_TEST_NAME}"
    DATASET_DIR = "news-elpais-grupoz-annotated-impacts/"
    DATASET_BASE_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/"
    DATASET_PATH = f"{DATASET_BASE_PATH}/sample/"
    ANNOTATION_PATH = f"{DATASET_BASE_PATH}/all.csv"
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
            "impact_extraction": "impact_extraction_parser_description_es",
            "impact_response_parser": None,
        },
    }

    test = ClimateImpactExtractorTest(
        TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG
    )
    test.run()

    # TODO handle not evaluation per sentence, rather per article
    evaluation = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "impact")
    evaluation.run()
