from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation


DATASET_DIR = "news-elpais-sample-194-annotated-e2e"
DATASET_BASE_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/"

SHORT_TEST = False
# TODO
if not SHORT_TEST:
    DATASET_DIR = "news-elpais-sample-194-annotated-e2e"
    DATASET_BASE_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/"
    DATASET_PATH = f"{DATASET_BASE_PATH}/sample/"
    # DATASET_PATH = f"{DATASET_BASE_PATH}/sample-pred-drought/"
    ANNOTATION_PATH = f"{DATASET_BASE_PATH}/dataset.csv"
else:
    DATASET_BASE_PATH = (
        "/home/javier/Developer/SeqIA/data/test-datasets-small/test-jvela-1/"
    )
    DATASET_PATH = f"{DATASET_BASE_PATH}/sample"
    # DATASET_PATH = "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-5T-2F/sample"
    ANNOTATION_PATH = f"{DATASET_BASE_PATH}/labels.csv"

BASE_TEST_NAME = f"news-elpais-e2e-impacts-prompt-engineering"


################################################################################
# Test: Extraction (with response parsing)
################################################################################

TEST_NAME = f"{BASE_TEST_NAME}/extraction-json"
OVERRIDE_CONFIG = {
    "pipeline": {
        "summarization": {"enable": False},
        "response_parsing": {"enable": False},
    },
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


################################################################################
# Test: Summarization + Extraction (with response parsing)
################################################################################

TEST_NAME = f"{BASE_TEST_NAME}/summarization-extraction-json"
OVERRIDE_CONFIG = {
    "pipeline": {
        "summarization": {"enable": True},
        "response_parsing": {"enable": False},
    },
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


################################################################################
# Test: Extraction + Response Parsing
################################################################################

TEST_NAME = f"{BASE_TEST_NAME}/extraction-response-parsing"
OVERRIDE_CONFIG = {
    "pipeline": {
        "summarization": {"enable": False},
        "response_parsing": {"enable": True},
    },
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


################################################################################
# Test: Summarization + Extraction + Response Parsing
################################################################################

TEST_NAME = f"{BASE_TEST_NAME}/summarization-extraction-response-parsing"
OVERRIDE_CONFIG = {
    "pipeline": {
        "summarization": {"enable": True},
        "response_parsing": {"enable": True},
    },
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
