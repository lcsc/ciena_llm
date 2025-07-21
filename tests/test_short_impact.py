from common import ClimateImpactExtractorTest


TEST_NAME = "test_short_impact"
DATASET_BASE_PATH = (
    "/home/javier/Developer/SeqIA/data/test-datasets-small/news-elpais-binary-2T-1F/"
)
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "gemma3:4b"
STRUCTURED_OUTPUT_MODE = "prompt"

OVERRIDE_CONFIG = {
    "extraction_task": "impact",
    "llm": {
        "name": MODEL,
        "structured_output_mode": STRUCTURED_OUTPUT_MODE,
    },
    "steps": {
        "summarization": {
            "enable": False,
            "prompt": {"language": LANGUAGE},
        },
        "extraction": {
            "enable": True,
            "prompt": {
                "language": LANGUAGE,
                "category": "description",
                "cot": True,
            },
        },
        "self_criticism": {
            "enable": False,
            "prompt": {
                "language": LANGUAGE,
            },
        },
        "response_parsing": {
            "enable": True,
            "prompt": {
                "language": LANGUAGE,
            },
        },
    },
    "event": {
        "tag": "drought",
        "text_en": "drought",
    },
    "impacts": [
        {
            "tag": "agriculture",
            "text_en": "agriculture",
            "description_en": "News about the impacts of drought on agriculture usually refer to losses in both rainfed and irrigated crops. It is often mentioned that part of the harvest has been lost or will be lost.",
        },
        {
            "tag": "livestock",
            "text_en": "livestock",
            "description_en": "News about the impacts of drought on livestock usually refer to the loss of pastures that feed the livestock. In more extreme droughts, it may be mentioned that there is no water available to give the livestock to drink.",
        },
        {
            "tag": "hydrological_resources",
            "text_en": "hydrological resources",
            "description_en": "News about the impacts of drought on hydrological resources usually mention the decrease in river flows, reservoir levels, or groundwater. It is also mentioned the lack of water that this causes in the populations, with water cuts being decreed or water not being used for certain uses, or the need to bring water from other locations.",
        },
        {
            "tag": "energy",
            "text_en": "energy",
            "description_en": "News about the impacts of drought on energy usually mention that due to the low flow of rivers or reservoirs, it is not possible to turbine and therefore the generation of hydroelectric energy decreases.",
        },
    ],
}

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG)
test.run()
