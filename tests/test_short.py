from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation


TEST_NAME = "test_short"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-5T-2F/"
)
DATASET_DIR = f"{DATASET_BASE_PATH}/sample"
ANNOTATION_PATH = f"{DATASET_BASE_PATH}/labels.csv"

OVERRIDE_CONFIG = {
    "pipeline": {
        "drought": {
            "enable": True,
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
        "default": {"name": "llama3.1:8b"},
    },
    "prompt": {
        "drought_classification": "drought_classification_en",
        "drought_response_parser": "drought_response_parser_en",
        "impact_classification": "impact_classification_parser_description_en",
        "impact_response_parser": None,
    },
}


test = ClimateImpactExtractorTest(
    TEST_NAME, DATASET_BASE_PATH, DATASET_DIR, OVERRIDE_CONFIG
)
test.run()

eval_drought = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "drought")
eval_drought.run()

eval_impact = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "impact")
eval_impact.run()
