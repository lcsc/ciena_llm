import json
import logging

from langchain_community.llms import Ollama

from seqia_gen.article import text2
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
    extracted_info = extract_drought_info(text2)
    print(extracted_info)


if __name__ == "__main__":
    main()
