import os

from common import ClimateImpactExtractorTest
from ciena_llm.article import Article
from ciena_llm.article.loader import ArticleLoader
from typing import List

TEST_NAME = "test_hail_event"
DATASET_BASE_PATH = os.getenv("DATASET_BASE_PATH")
DATASET_PATH = f"{DATASET_BASE_PATH}/sample"

LANGUAGE = "en"
MODEL = "gemma3:4b"
STRUCTURED_OUTPUT_MODE = "prompt"

OVERRIDE_CONFIG = {
    "extraction_task": "hail_event",
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
        "tag": "hail",
        "text_en": "hail",
    },
}

class CustomArticleLoader(ArticleLoader):
    def __init__(self):
        super().__init__()
    
    def __call__(
        self,
        path: str = None,
        file_list: List[str] = None,
    ) -> List[Article]:
        print(f"Loading first 10 articles from {path}")
        ret = super().__call__(path,file_list)
        return ret[0:10]

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG,article_loader=CustomArticleLoader())
test.run()
