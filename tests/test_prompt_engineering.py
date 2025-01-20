from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation


DATASET_DIR = "news-elpais-sample-194-annotated-e2e"
DATASET_BASE_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/"

BASE_TEST_NAME = "prompt-engineering"

TEST_TYPE = "impacts"  # "e2e" or "impacts" or "short"


if TEST_TYPE == "e2e":
    DATASET_DIR = "news-elpais-sample-194-annotated-e2e"
    DATASET_BASE_PATH = f"/home/javier/Developer/SeqIA/data/{DATASET_DIR}/"
    DATASET_PATH = f"{DATASET_BASE_PATH}/sample/"
    # DATASET_PATH = f"{DATASET_BASE_PATH}/sample-pred-drought/"
    ANNOTATION_PATH = f"{DATASET_BASE_PATH}/dataset.csv"
    BASE_TEST_NAME = f"{BASE_TEST_NAME}/e2e"
elif TEST_TYPE == "impacts":
    DATASET_BASE_PATH = (
        "/home/javier/Developer/SeqIA/data/news-elpais-grupoz-annotated-impacts/"
    )
    DATASET_PATH = f"{DATASET_BASE_PATH}/sample"
    ANNOTATION_PATH = f"{DATASET_BASE_PATH}/all.csv"
    BASE_TEST_NAME = f"{BASE_TEST_NAME}/impacts"
elif TEST_TYPE == "short":
    DATASET_BASE_PATH = (
        "/home/javier/Developer/SeqIA/data/test-datasets-small/test-jvela-1/"
    )
    DATASET_PATH = f"{DATASET_BASE_PATH}/sample"
    # DATASET_PATH = "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-5T-2F/sample"
    ANNOTATION_PATH = f"{DATASET_BASE_PATH}/labels.csv"
    BASE_TEST_NAME = f"{BASE_TEST_NAME}/short"
else:
    raise ValueError(f"Unknown TEST_TYPE: {TEST_TYPE}")


def run_test(test_name_suffix, summarization_enable, response_parsing_enable, language):
    TEST_NAME = f"{BASE_TEST_NAME}/{test_name_suffix}-{language}"
    OVERRIDE_CONFIG = {
        "task": "impact",
        "pipeline": {
            "summarization": {
                "enable": summarization_enable,
                "prompt": {
                    "language": language,
                },
            },
            "response_parsing": {
                "enable": response_parsing_enable,
                "prompt": {
                    "language": language,
                },
            },
        },
        "llm": {
            "default": {"name": "gemma2:9b"},
        },
    }

    test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
    test.run()

    # TODO parametrize based on test hacing drought label or not. Or just check in text and return None if not found
    # eval_drought = ClimateImpactExtractorEvaluation(
    #     TEST_NAME, ANNOTATION_PATH, "drought"
    # )
    # eval_drought.run()

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
