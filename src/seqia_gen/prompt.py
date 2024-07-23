from langchain.prompts import PromptTemplate


custom_prompt = """
Por favor, analiza el siguiente texto y extrae la información relacionada con la sequía climatológica, sus impactos, y la localización y la cuantificación de los impactos.
Los impactos que se deben extraer son cualquiera de los mencionados en la siguiente lista: {impacts}
La cuantificación de los impactos es, por ejemplo, la cantidad de dinero, la cantidad de agua, el cultivo afectado, etc.
Extraee cada uno de los impactos en una estructura de la siguiente manera:
{{
	"sentence": "frase que contiene el impacto",
	"impact": "impacto",
	"location": "localización",
	"quantification": "cuantificación"
}}
Estructura la información estrictamente en formato JSON de la siguiente manera y no incluyas ninguna otra explicación:
{{
    "drought": "True/False",
    "impacts": [] // Lista de impactos con la estructura mencionada
}}
Si bien no hay menciones a la sequía climatológica, por favor, responde con: 
{{
    "drought": "False",
    "impacts": []
}}
Quiero que la respuesta sea únicamente un JSON válido. Por lo que no añadas ningún otro texto adicional.
Texto:
{text}
"""


# Create the prompt template
prompt = PromptTemplate(template=custom_prompt, input_variables=["text", "impacts"])
