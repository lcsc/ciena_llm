from langchain.prompts import PromptTemplate


custom_prompt = """
Por favor, analiza el siguiente texto y extrae la información relacionada con la sequía climatológica, sus impactos y la localización de los impactos.
Estructura la información estrictamente en formato JSON de la siguiente manera y no incluyas ninguna otra explicación:
{{
    "drought": "True/False",
    "impacts": [] // Lista de impactos con la estructura mencionada a continuación
}}
Únicamente incluye impactos si existen menciones a la sequía climatológica.
Si bien no hay menciones a la sequía climatológica, por favor, responde con: 
{{
    "drought": "False",
    "impacts": []
}}
Extraee cada uno de los impactos en una estructura de la siguiente manera:
{{
	"impact_class": "impact class",
	"impact": "impact description",
	"location": [{{"name": "location","type": "location_type"}}, ... ],
}}
A los impactos extraídos asignales una clase ("impact_class") de la siguiente lista: {impacts}.
Si bien uno de los impactos no aparece, puedes añadirlo en una clase "other" y poner entre paréntesis la nueva clase que tú le asignarías de la siguiente manera: "other (new impact class)"
En el campo "impact" inserta una descripción corta del impacto.
En el campo "location" inserta una lista de las localizaciones afectadas por el impacto. Por cada localización inserta su nombre "name" y tipo de localización "type". Es posible que localizaciones con el mismo nombre se refieran a tipos diferentes (provincia/ciudad). Ejemplos: Comunidad de Madrid (tipo: comunidad autonoma), Zaragoza (provincia o municipio), Ebro (rio o cuenca).
Quiero que la respuesta sea únicamente un JSON válido y de la misma estructura que la mencionada. Por lo que no añadas ningún otro texto adicional.
Texto:
{text}
"""


# Create the prompt template
prompt = PromptTemplate(template=custom_prompt, input_variables=["text", "impacts"])
