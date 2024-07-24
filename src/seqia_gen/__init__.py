import json
import logging
import os
from typing import Optional
from tqdm import tqdm

import dotenv

dotenv.load_dotenv()
from langchain_community.llms import Ollama
from seqia.article import Article
from seqia.article.loader import ArticleLoader
from seqia.utils.output import write_summary_to_csv

from seqia_gen.prompt import prompt
from seqia_gen.response import parse_response

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


TEST_NAME = "news-elpais-binary-50T-50F"
# TEST_NAME = "news-elpais-binary-50T-50F"
DATASET_PATH = (
    f"/home/javier/Developer/SeqIA/data/test-datasets-small/{TEST_NAME}/sample"
)
RESULTS_DIR = f"./results/{TEST_NAME}/"
os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)


# Initialize the Ollama model
llm = Ollama(model="llama3")

# Create the LangChain with the LLM and the prompt template
chain = prompt | llm

impacts = [
    "agriculture",
    "farming",
    "hidrological_resources",
    "energy",
    "other",
]


def extract(article: Article) -> Optional[Article]:
    text = article.get_headline_and_body(separator=".")
    response = chain.invoke({"text": text, "impacts": impacts})
    article, parsed = parse_response(article, response)

    if parsed:
        return article


def main():
    loader = ArticleLoader()
    articles = loader(DATASET_PATH)

    loader.write_excluded_problematic_articles_to_csv(f"{RESULTS_DIR}/excluded.csv")

    for article in tqdm(articles, desc="Extracting impacts from articles."):
        article = extract(article)

        if article:
            logging.debug(f"Article {article.filename}:\n{article}")

    write_summary_to_csv(
        articles,
        f"{RESULTS_DIR}/summary.csv",
        [
            "article_filename",
            "article_drought",
            "article_impacts_aggregated",
            "article_locations_aggregated",
            "article_locations_aggregated",
            "article_date",
            "article_url",
            "article_headline",
        ],
    )


if __name__ == "__main__":
    main()
