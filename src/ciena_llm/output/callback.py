from ..article import Article

class ClimateImpactExtractorCallback:
    def __init__(self):
        pass

    def start(self, article:Article):
        pass
    def __call__(self, article: Article, step: str, data: any):
        pass
    
    def summary(self, article:Article, data:any):
        self(article, "summarization", data)
        pass
    
    def extraction(self, article:Article, data:any):
        self(article, "extraction", data)
        pass
    
    def self_criticism(self, article:Article, data:any):
        self(article, "self_criticism", data)
        pass
    
    def response_parsing(self, article:Article, data:any):
        self(article, "response_parsing", data)
        pass

    def end(self, article:Article):
        pass