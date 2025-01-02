from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation


DATASET_DIR = "news-elpais-sample-194-annotated-e2e"
DATASET_BASE_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/"
DATASET_PATH = f"{DATASET_BASE_PATH}/sample-pred-drought/"
ANNOTATION_PATH = f"{DATASET_BASE_PATH}/dataset.csv"


TEST_NAME = f"news-elpais-e2e-impacts-non-summarization"
OVERRIDE_CONFIG = {
    "pipeline": {"summarization": {"enable": False}},
    "llm": {
        "default": {"name": "gemma2:9b"},
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()

eval_drought = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "drought")
eval_drought.run()

eval_impact = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "impact")
eval_impact.run()


TEST_NAME = f"news-elpais-e2e-impacts-summarization"
OVERRIDE_CONFIG = {
    "pipeline": {"summarization": {"enable": True}},
    "llm": {
        "default": {"name": "gemma2:9b"},
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()

eval_drought = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "drought")
eval_drought.run()

eval_impact = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "impact")
eval_impact.run()
