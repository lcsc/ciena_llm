import json
import logging

from langchain_community.llms import Ollama
from seqia.article.loader import ArticleLoader

from seqia_gen.prompt import prompt

# Setup logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Initialize the Ollama model
llm = Ollama(model="llama3")

# Create the LangChain with the LLM and the prompt template
chain = prompt | llm

impacts = [
    "agriculture",
    "farming",
    "hidrological_resources",
    "energy",
    "economy",
    "social",
]


def extract_drought_info(text):
    # Call the chain with the provided text
    response = chain.invoke({"text": text, "impacts": impacts})

    logging.debug(f"Response: {response}")

    # Load the response as a JSON object
    try:
        result = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        result = {}

    return result


def main():
    loader = ArticleLoader()
    articles = loader(
        "/home/javier/Developer/SeqIA/data/test-datasets-small/test-jvela-00-10/"
    )
    for article in articles:
        extracted_info = extract_drought_info(
            article.get_headline_and_body(separator=".")
        )
        print(f"Article {article.filename}:\n{extracted_info}")


if __name__ == "__main__":
    main()
