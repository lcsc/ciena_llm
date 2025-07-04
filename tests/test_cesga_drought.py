from common import ClimateImpactExtractorTest, ClimateImpactExtractorEvaluation

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

ANNOTATION_PATH = os.getenv("ANNOTATION_PATH")

LANGUAGE = os.getenv("CIENA_LLM_LANGUAGE", "en")
MODEL = os.getenv("CIENA_LLM_MODEL", "llama3.2:3b")

SUMMARIZATION_ENABLE = (
    os.getenv("CIENA_LLM_SUMMARIZATION_ENABLE", "True").lower() == "true"
)
EVENT_IDENTIFICATION_ENABLE = (
    os.getenv("CIENA_LLM_EVENT_IDENTIFICATION_ENABLE", "False").lower() == "true"
)
IMPACT_EXTRACTION_ENABLE = (
    os.getenv("CIENA_LLM_IMPACT_EXTRACTION_ENABLE", "True").lower() == "true"
)
LOCATION_EXTRACTION_ENABLE = (
    os.getenv("CIENA_LLM_LOCATION_EXTRACTION_ENABLE", "True").lower() == "true"
)
RESPONSE_PARSING_ENABLE = (
    os.getenv("CIENA_LLM_RESPONSE_PARSING_ENABLE", "True").lower() == "true"
)
COT_ENABLE = os.getenv("CIENA_LLM_COT_ENABLE", "False").lower() == "true"
SELF_CRITICISM_ENABLE = (
    os.getenv("CIENA_LLM_SELF_CRITICISM_ENABLE", "False").lower() == "true"
)
IMPACT_PROMPT_CATEGORY = os.getenv("CIENA_LLM_IMPACT_PROMPT_CATEGORY", "simple")
STRUCTURED_OUTPUT_MODE = os.getenv("CIENA_LLM_STRUCTURED_OUTPUT_MODE", "tool").lower()

OVERRIDE_CONFIG = {
    "llm": {
        "name": MODEL,
        "structured_output_mode": STRUCTURED_OUTPUT_MODE,
    },
    "stages": {
        "summarization": {
            "enable": SUMMARIZATION_ENABLE,
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
            "enable": EVENT_IDENTIFICATION_ENABLE,
            "steps": {
                "extraction": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
                        "step": "extraction",
                        "cot": COT_ENABLE,
                    },
                },
                "self_criticism": {
                    "enable": SELF_CRITICISM_ENABLE,
                    "prompt": {
                        "language": LANGUAGE,
                    },
                },
                "response_parsing": {
                    "enable": RESPONSE_PARSING_ENABLE,
                    "prompt": {
                        "language": LANGUAGE,
                    },
                },
            },
        },
        "impact_extraction": {
            "enable": IMPACT_EXTRACTION_ENABLE,
            "steps": {
                "extraction": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
                        "step": "extraction",
                        "category": IMPACT_PROMPT_CATEGORY,
                        "cot": COT_ENABLE,
                    },
                },
                "self_criticism": {
                    "enable": SELF_CRITICISM_ENABLE,
                    "prompt": {
                        "language": LANGUAGE,
                    },
                },
                "response_parsing": {
                    "enable": RESPONSE_PARSING_ENABLE,
                    "prompt": {
                        "language": LANGUAGE,
                    },
                },
            },
        },
        "location_extraction": {
            "enable": LOCATION_EXTRACTION_ENABLE,
            "steps": {
                "extraction": {
                    "enable": True,
                    "prompt": {
                        "language": LANGUAGE,
                        "step": "extraction",
                        "category": "province",
                        "cot": COT_ENABLE,
                    },
                },
                "self_criticism": {
                    "enable": SELF_CRITICISM_ENABLE,
                    "prompt": {
                        "language": LANGUAGE,
                    },
                },
                "response_parsing": {
                    "enable": RESPONSE_PARSING_ENABLE,
                    "prompt": {
                        "language": LANGUAGE,
                        "category": "province",
                    },
                },
            },
        },
    },
    "event": {
        "tag": "drought",
        "text_es": "sequía",
        "text_en": "drought",
        "description_es": "Noticias sobre sequías suelen hacer referencia a la falta de lluvias, a la disminución de los caudales de los ríos, a la disminución de los niveles de los embalses o a la disminución de las aguas subterráneas.",
        "description_en": "News about droughts usually refer to the lack of rain, the decrease in river flows, the decrease in reservoir levels, or the decrease in groundwater.",
    },
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG, RESULTS_DIR)
test.run()

if ANNOTATION_PATH:
    evaluation = ClimateImpactExtractorEvaluation(
        TEST_NAME, ANNOTATION_PATH, "impact", RESULTS_DIR
    )
    evaluation.run()
