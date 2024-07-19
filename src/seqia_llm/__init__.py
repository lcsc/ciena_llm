from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import json

# Initialize the Ollama model
llm = Ollama(model="llama3")

custom_prompt = """
Por favor, analiza el siguiente texto y extrae la información relacionada con la sequía meteorológica y sus impactos. Estructura la información estrictamente en formato JSON de la siguiente manera y no incluyas ninguna otra explicación:

{{
    "drought": "True/False",
    "impacts": ["impact1", "impact2", "impact3"]
}}

Texto:
{text}
"""


# Create the prompt template
prompt = PromptTemplate(template=custom_prompt, input_variables=["text"])

# Create the LangChain with the LLM and the prompt template
chain = prompt | llm


def extract_drought_info(text):
    # Call the chain with the provided text
    response = chain.invoke({"text": text})

    # Load the response as a JSON object
    try:
        result = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        result = {}

    return result


# Example usage
spanish_text = """
El artículo discute las condiciones climáticas recientes en España. 
Se menciona una sequía meteorológica que ha afectado varias regiones, 
provocando una reducción significativa en las reservas de agua y 
afectando la agricultura y el suministro de agua potable.
"""


def main():
    extracted_info = extract_drought_info(spanish_text)
    print(extracted_info)


if __name__ == "__main__":
    main()
