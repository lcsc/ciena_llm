from common import ClimateImpactExtractorTest

TEST_NAME = "news-elpais-1990-provinces"
DATASET_DIR = "news-elpais-all-1990-drought-impact"
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
            "name": "gemma2:27b",  # TODO "llama3.1:8b", "llama3.1:70b", "llama3.2:3b", "mistral-small:22b", "gemma2:9b", "gemma2:27b", "qwen2.5:32b" ?
        },
    },
    "prompt": {
        "province_extraction": "provinces_extraction_parser_en",
        "province_response_parser": None,
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_DIR, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
