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


def run_test(test_name_suffix, summarization_enable, response_parsing_enable, language):
    TEST_NAME = f"{BASE_TEST_NAME}/{test_name_suffix}-{language}"
    if SHORT_TEST:
        TEST_NAME = f"{TEST_NAME}-short"
    OVERRIDE_CONFIG = {
        "pipeline": {
            "summarization": {
                "enable": summarization_enable,
                "language": language,
            },
            "response_parsing": {
                "enable": response_parsing_enable,
                "language": language,
            },
        },
        "llm": {
            "default": {"name": "gemma2:9b"},
        },
    }

    test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
    test.run()

    eval_drought = ClimateImpactExtractorEvaluation(
        TEST_NAME, ANNOTATION_PATH, "drought"
    )
    eval_drought.run()

    eval_impact = ClimateImpactExtractorEvaluation(TEST_NAME, ANNOTATION_PATH, "impact")
    eval_impact.run()


for language in ["en", "es"]:

    ############################################################################# Test: Extraction (with response parsing)
    ############################################################################
    run_test(
        "extraction-json",
        summarization_enable=False,
        response_parsing_enable=False,
        language=language,
    )

    ############################################################################
    # Test: Summarization + Extraction (with response parsing)
    ############################################################################
    run_test(
        "summarization-extraction-json",
        summarization_enable=True,
        response_parsing_enable=False,
        language=language,
    )

    ############################################################################
    # Test: Extraction + Response Parsing
    ############################################################################
    run_test(
        "extraction-response-parsing",
        summarization_enable=False,
        response_parsing_enable=True,
        language=language,
    )

    ############################################################################
    # Test: Summarization + Extraction + Response Parsing
    ############################################################################
    run_test(
        "summarization-extraction-response-parsing",
        summarization_enable=True,
        response_parsing_enable=True,
        language=language,
    )
