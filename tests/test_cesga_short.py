from common import ClimateImpactExtractorTest

import os
import sys
from datetime import datetime


HOME = os.getenv("HOME")
CIENA_LLM_DIR = os.getenv("CIENA_LLM_DIR", f"{HOME}/CienaLLM")
TEST_NAME = os.getenv("TEST_NAME", "test_cesga_short")

results_dir_default = (
    f"{CIENA_LLM_DIR}/ciena_llm/results/"
    + TEST_NAME
    + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
)
RESULTS_DIR = os.getenv("RESULTS_DIR", results_dir_default)

DATASET_PATH = os.getenv("DATASET_PATH")
if not DATASET_PATH or not os.path.exists(DATASET_PATH):
    print("DATASET_PATH not set or does not exist. Exiting.")
    sys.exit(1)


LANGUAGE = os.getenv("CIENA_LLM_LANGUAGE", "en")
MODEL = os.getenv("CIENA_LLM_MODEL", "llama3.2:3b")

OVERRIDE_CONFIG = {
    "llm": {"name": MODEL},
    "stages": {
        "summarization": {
            "enable": True,
            "steps": {
                "summarization": {
                    "enable": True,
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

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG, RESULTS_DIR)
test.run()
