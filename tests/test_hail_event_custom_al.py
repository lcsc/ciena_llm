import os

from common import ClimateImpactExtractorTest
from ciena_llm.article import Article
from ciena_llm.article.loader import ArticleLoader
from ciena_llm.output.callback import ClimateImpactExtractorCallback
from typing import List
import json

from pydantic import BaseModel

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

class CustomCB(ClimateImpactExtractorCallback):
    def __init__(self):
        super().__init__()
        self.path=None
    
    def setPath(self, path: str):
        self.path=path  
        os.makedirs(f"{self.path}/cb", exist_ok=True)

    def _get_filename(self, article:Article):
        filename = article.filename
        if filename.endswith(".json"):
            filename = filename[:-5]
        if filename.startswith(DATASET_PATH):
            filename = filename[len(DATASET_PATH)+1:]
        return filename

    def start(self, article: Article):
        pass    
    
    def _dump(self,data:any)->any:
        if isinstance(data, dict):
            ret = {}
            for key,value in data.items():
                ret[key]=self._dump(value) 
            return ret
        elif isinstance(data, list):
            return [self._dump(v) for v in data]
        elif isinstance(data, BaseModel):
            return data.model_dump()
        else:
            return data 

    def __call__(self, article: Article, step: str, data: any):
        print(f"Step {step} finished for article {self._get_filename(article)}")
        with open(f"{self.path}/cb/{self._get_filename(article)}.{step}.json", "w") as f:
            json.dump(self._dump(data), f, indent=2)
        pass

    def end(self, article:Article):
        pass

cb = CustomCB()

test = ClimateImpactExtractorTest(TEST_NAME, DATASET_PATH, OVERRIDE_CONFIG,article_loader=CustomArticleLoader(), callbacks=[cb])
cb.setPath(test.results_dir)

test.run()
