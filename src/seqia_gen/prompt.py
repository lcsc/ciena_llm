from langchain.prompts import PromptTemplate


custom_prompt = """
Por favor, analiza el siguiente texto y extrae la información relacionada con la sequía climatológica, sus impactos y la localización de los impactos.
Estructura la información estrictamente en formato JSON de la siguiente manera sin incluir ninguna otra explicación:
{{
    "drought": "True/False",
    "impacts": []
}}
Solo incluye impactos si hay menciones a la sequía climatológica. Si no hay menciones a la sequía climatológica, responde con:
{{
    "drought": "False",
    "impacts": []
}}
Extrae cada uno de los impactos en la siguiente estructura:
{{
    "impact_class": "impact class",
    "impact": "impact description",
    "location": [{{"name": "location", "type": "location_type"}}, ...]
}}
Asigna cada impacto a una clase ("impact_class") de la siguiente lista: {impacts}.
Si uno de los impactos no aparece, añádelo en una clase "other" y pon entre paréntesis la nueva clase que tú le asignarías de la siguiente manera: "other (clase)".
En el campo "impact" incluye una descripción muy breve del impacto.
En el campo "location" incluye una lista de las localizaciones afectadas por el impacto. Para cada localización, incluye su nombre "name" y tipo de localización "type". Es posible que localizaciones con el mismo nombre se refieran a tipos diferentes (e.g. provincia o ciudad). Ejemplos: Comunidad de Madrid (comunidad autónoma), Zaragoza (provincia), Ebro (río), cuenca del Duero (cuenca).
Quiero que la respuesta sea únicamente un JSON válido con la estructura mencionada. No añadas ningún otro texto adicional.
Texto:
{text}
"""

# Create the prompt template
prompt = PromptTemplate(template=custom_prompt, input_variables=["text", "impacts"])
