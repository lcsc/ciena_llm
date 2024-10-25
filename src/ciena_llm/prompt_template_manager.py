import json
from typing import List

from langchain_core.prompts import PromptTemplate

DROUGHT_EXTRACTION_BOOL_ES = """
Analiza el siguiente artículo y determina si la noticia está relacionada con la sequía climática.
Texto:
{text}
Por ejemplo, si el artículo está relacionado con la sequía climática, responde únicamente la palabra "True" y si no lo está, responde "False". No añadas ningún signo de puntuación ni proporciones ninguna explicación adicional. Sólo True/False.
"""

DROUGHT_EXTRACTION_ES = """
Analiza el siguiente artículo y determina si la noticia está relacionada con la sequía climática.
Texto:
{text}
"""

DROUGHT_EXTRACTION_EN = """
Analyze the following article and determine if the news article is mentions the existance of climate drought.
In your response, provide only an affirmative or negative answer.
Text:
{text}
"""

IMPACT_EXTRACTION_BOOL_ES = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina si esta noticia menciona un impacto de la sequía en {impact}.
Texto:
{text}
Por ejemplo, si el artículo menciona un impacto en {impact}, responde únicamente la palabra "True" y si no lo está, responde "False". No añadas ningún signo de puntuación ni proporciones ninguna explicación adicional. Sólo True/False.
"""

IMPACT_EXTRACTION_ES = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina si esta noticia menciona un impacto de la sequía en {impact}.
Texto:
{text}
"""

IMPACT_EXTRACTION_EN = """
Analyze the following article related to climate drought. Determine if this news article mentions an impact of the drought on {impact}.
In your response, provide only an affirmative or negative answer.
Text:
{text}
"""

LOCATION_EXTRACTION_ES = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina las localizaciones que aparecen en el texto que impactadas por la sequía. Además, indica a que tipo de localización se refiere (e.g. municipio, provincia, comunidad autonoma, río, presa, cuenca, etc.). Lista únicamente aquellas que estén directamente relacionadas con la sequía. Por localización, indica una pequeña descripción del impacto de la sequía en esa localización según la noticia. En el caso de que no haya ninguna localización impactada por la sequía, no menciones ninguna.
Texto:
{text}
"""

LOCATION_EXTRACTION_EN = """
Analyze the following article related to climate drought.
Determine the named geographical locations mentioned in the text that are directly impacted by the drought.
If no locations are impacted by the drought, do not return any output.
For each impacted location, provide the following information:
- The proper name of the location without additional descriptive text.
- The type of location (e.g., municipality, province, autonomous community, river, dam, basin, etc.). Only assign one type.
- A brief description of the drought's impact on that location.
- The list of provinces or equivalent administrative division where the location is situated, if mentioned or inferable. In the case of multiple provinces impacted, list them all. 
Text:
{text}
"""

LOCATION_PROVINCES_EXTRACTION_EN = """
Analyze the following news article related to climate drought.
Determine the named locations and geographical accidents impacted by the drought according to the text.
If a location is not impacted by the drought, do not list it.
Return the names for the locations and the provinces in Spanish.
It is possible that some locations are not directly mentioned in the text. In these cases, you should infer the location based on the context of the article. If you are unable to infer the location, do not include it in the output.
For each impacted location, provide the following information:
1. The toponym of the location or geographical accident. 
    It is not necessary to extract the name as it appears in the text.
    Give the location proper name without additional descriptive text  
    Do not list a general location type as a specific toponym.
    Examples (1): 
    - "Ebro" instead of "el río Ebro" and "Yesa" instead of "el pantano de Yesa", and include the type in the location type field.
    - Do not list "río" as a location as it is not a specific toponym.
2. The type of location. Only return a single type for each location. If the location could be many different types, infer which one is the most appropriate based on the context.
    Examples (2):
    - "river" for "Ebro"
    - "dam" for "el pantano de Yesa"
    - "basin" for "la cuenca del Ebro"
    - "province" instead of "province/municipality" if the article is about the province
3. The list of provinces impacted where the location are situated, if mentioned or inferable. In the case of multiple provinces impacted, list them all. If the location is a province, include the province in the list of provinces. If the location has multiple provinces, only include the impacted provinces.
    In Spain, provinces are the primary subnational administrative divisions within autonomous communities. Each province consists of multiple municipalities and serves as a local government structure, below the national and regional (autonomous community) levels. Spain is divided into 50 provinces. Provinces should not be confused with autonomous communities, which are larger political entities that may include several provinces within their borders.
    Return a list of provinces as strings, for all the locations. If the location is a province, include the province in the list of provinces.
    Examples (3):
    - "Cantabria, Palencia, Burgos, Álava, La Rioja, Navarra, Zaragoza, Huesca, Lérida, Tarragona" for "Ebro" if the article is about the Ebro River in Spain
    - "Tarragona" for "Ebro" if the article is about the mouth of the Ebro River in Spain
    - "Sevilla, Cádiz" instead of "Almería, Cádiz, Córdoba, Granada, Huelva, Jaén, Málaga, Sevilla" for "Andalucía" if the article only mentions impacts in Sevilla and Cádiz
Text:
{text}
"""


BOOLEAN_RESPONSE_PARSER_EN = """
Extract whether the following text is affirmative or negative.
Format instructions:
{format_instructions}
Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
Text:
{text}
"""

DROUGHT_RESPONSE_PARSER_EN = """
Extract whether the following text is related to climate drought.
Format instructions:
{format_instructions}
Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
Text:
{text}
"""

IMPACT_RESPONSE_PARSER_EN = """
Extract whether the following text mentions an impact of climate drought on {impact}.
Format instructions:
{format_instructions}
Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
Text:
{text}
"""

LOCATION_RESPONSE_PARSER_EN = """
Extract the locations impacted by climate drought from the given text.
The output must be a valid JSON object formatted according to the schema, including any optional fields where applicable.
Format instructions:
{format_instructions}
For each location, include all properties as specified in the schema, including optional ones, if they appear in the text.
If there are no locations impacted by the climate drought, provide an empty JSON object.
Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
Do not encode any special characters and do not use any Unicode escape sequences in the output.
Text:
{text}
"""


class PromptTemplateManager:
    def __init__(self):
        self.templates = {
            "drought_extraction_es": {
                "template": DROUGHT_EXTRACTION_ES,
                "variables": ["text"],
            },
            "drought_extraction_bool_es": {
                "template": DROUGHT_EXTRACTION_BOOL_ES,
                "variables": ["text"],
            },
            "drought_extraction_en": {
                "template": DROUGHT_EXTRACTION_EN,
                "variables": ["text"],
            },
            "impact_extraction_es": {
                "template": IMPACT_EXTRACTION_ES,
                "variables": ["text", "impact"],
            },
            "impact_extraction_bool_es": {
                "template": IMPACT_EXTRACTION_BOOL_ES,
                "variables": ["text"],
            },
            "impact_extraction_en": {
                "template": IMPACT_EXTRACTION_EN,
                "variables": ["text"],
            },
            "location_extraction_es": {
                "template": LOCATION_EXTRACTION_ES,
                "variables": ["text"],
            },
            "location_extraction_en": {
                "template": LOCATION_EXTRACTION_EN,
                "variables": ["text"],
            },
            "location_provinces_extraction_en": {
                "template": LOCATION_PROVINCES_EXTRACTION_EN,
                "variables": ["text"],
            },
            "boolean_response_parser_en": {
                "template": BOOLEAN_RESPONSE_PARSER_EN,
                "variables": ["text"],
                "partial_variables": ["format_instructions"],
            },
            "drought_response_parser_en": {
                "template": DROUGHT_RESPONSE_PARSER_EN,
                "variables": ["text"],
                "partial_variables": ["format_instructions"],
            },
            "impact_response_parser_en": {
                "template": IMPACT_RESPONSE_PARSER_EN,
                "variables": ["text", "impact"],
                "partial_variables": ["format_instructions"],
            },
            "location_response_parser_en": {
                "template": LOCATION_RESPONSE_PARSER_EN,
                "variables": ["text"],
                "partial_variables": ["format_instructions"],
            },
        }

    def get_prompt_template(self, template_name: str, **kwargs) -> PromptTemplate:
        """
        Retrieves and returns a LangChain PromptTemplate for a given template name.

        :param template_name: The name of the template to retrieve.
        :param kwargs: Additional keyword arguments to format the template.
        :return: A LangChain PromptTemplate object.
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not recognized.")

        template_info = self.templates[template_name]
        template_str = template_info["template"]

        # Separate partial variables from input variables
        partial_vars = {
            k: v
            for k, v in kwargs.items()
            if k in template_info.get("partial_variables", [])
        }
        input_vars = {
            k: v
            for k, v in kwargs.items()
            if k not in template_info.get("partial_variables", [])
        }

        # Format the template string if there are any keyword arguments
        if input_vars:
            try:
                template_str = template_str.format(**input_vars)
            except KeyError as e:
                raise ValueError(f"Missing required argument for template: {e}") from e

        return PromptTemplate(
            template=template_str,
            input_variables=template_info["variables"],
            partial_variables=partial_vars,
        )
