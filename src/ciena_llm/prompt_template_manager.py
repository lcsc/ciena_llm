from langchain_core.prompts import PromptTemplate


DEFAULT = None

################################################################################
# Drough Classification
################################################################################

DROUGHT_CLASSIFICATION_BOOLEAN_ES = """
Analiza el siguiente artículo y determina si la noticia está relacionada con la sequía climática.
Texto:
{text}
Por ejemplo, si el artículo está relacionado con la sequía climática, responde únicamente la palabra "True" y si no lo está, responde "False". No añadas ningún signo de puntuación ni proporciones ninguna explicación adicional. Sólo True/False.
"""

DROUGHT_CLASSIFICATION_BOOLEAN_EN = """
Analyze the following article and determine if the news article is mentions the existance of climate drought.
In your response, provide only an affirmative or negative answer.
Text:
{text}
"""

DROUGHT_CLASSIFICATION_ES = """
Analiza el siguiente artículo y determina si la noticia está relacionada con la sequía climática.
Texto:
{text}
"""

DROUGHT_CLASSIFICATION_EN = """
Analyze the following article and determine if the news article is mentions the existance of climate drought.
Text:
{text}
"""


################################################################################
# Drough Extraction
################################################################################

# TODO


################################################################################
# Impact Classification
################################################################################

IMPACT_CLASSIFICATION_BOOLEAN_ES = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina si esta noticia menciona un impacto de la sequía en {impact}.
Texto:
{text}
Por ejemplo, si el artículo menciona un impacto en {impact}, responde únicamente la palabra "True" y si no lo está, responde "False". No añadas ningún signo de puntuación ni proporciones ninguna explicación adicional. Sólo True/False.
"""

IMPACT_CLASSIFICATION_BOOLEAN_EN = """
Analyze the following article related to climate drought. Determine whether the news article mentions an impact of drought on {impact}.
In your response, focus solely on the impact of the drought on {impact} as mentioned in the article.
In your response, provide only an affirmative or negative answer.
Text:
{text}
"""

IMPACT_CLASSIFICATION_ES = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina si esta noticia menciona un impacto de la sequía en {impact}.
Texto:
{text}
"""

IMPACT_CLASSIFICATION_EN = """
Analyze the following article related to climate drought. Determine whether the news article mentions an impact of drought on {impact}.
In your response, focus solely on the impact of the drought on {impact} as mentioned in the article.
Text:
{text}
"""

IMPACT_CLASSIFICATION_DESCRIPTION_EN = """
Analyze the following article related to climate drought. Determine whether the news article mentions an impact of drought on {impact}.
In your response, focus solely on the impact of the drought on {impact} as mentioned in the article.
The impact is defined as follows:
{impact_description}
Text:
{text}
Reason your answer and be brief. At the end of your response, provide a clear affirmative (True) or negative (False) answer.
"""

IMPACT_CLASSIFICATION_JSON_DESCRIPTION_EN = """
Analyze the following article related to climate drought. Determine whether the news article mentions an impact of drought on {impact}.
In your response, focus solely on the impact of the drought on {impact} as mentioned in the article.
The impact is defined as follows:
{impact_description}
Text:
{text}
Provide the only response in the following format:
Format instructions:
```json
{{"response": true or false}}
```
"""

IMPACT_CLASSIFICATION_JSON_DESCRIPTION_ES = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina si esta noticia menciona un impacto de la sequía en {impact}.
En tu respuesta, enfócate únicamente en el impacto de la sequía en {impact} tal como se menciona en el artículo.
El impacto se define como sigue:
{impact_description}
Texto:
{text}
Proporciona la única respuesta en el siguiente formato:
Instrucciones de formato:
```json
{{"response": true or false}}
```
"""

################################################################################
# Impact Extraction
################################################################################

IMPACT_EXTRACTION_JSON_ES = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina si la noticia menciona impactos de la sequía en los siguientes aspectos: {impacts}.
Para cada aspecto mencionado, proporciona la siguiente información:
1. Si el artículo menciona la sequía.
2. Si la sequía ha tenido un impacto en los aspectos mencionados.
Cada uno de los impactos se define de la siguiente manera:
{impact_descriptions}
Si el artículo no menciona ningún impacto de la sequía en los aspectos mencionados, no incluyas información adicional.
Texto:
{text}
Instrucciones de formato:
{format_instructions}
"""


################################################################################
# Location Extraction
################################################################################

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


################################################################################
# Provinces Extraction
################################################################################

PROVINCES_EXTRACTION_JSON_EN = """
Given a news article describing drought impacts in Spanish regions, return the list of affected provinces.
Identify provinces explicitly mentioned or infer them from the described locations.
If you cannot identify specific provinces, return all provinces in the regions mentioned.
Note that the text may refer to autonomous communities or specific cities, towns, and municipalities, which are not the provinces being requested. Do not include these autonomous communities or municipalities in the output.
Return the province names in Spanish.
Format instructions:
{format_instructions}
Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
Text:
{text}
"""
# Output the list as parsable JSON with the following structure.
# {"provinces":[]}
# Do not output anything else but the list of provinces.


################################################################################
# Boolean Response Parsers
################################################################################

BOOLEAN_RESPONSE_PARSER_EN = """
Extract whether the following text is affirmative or negative.
Format instructions:
{format_instructions}
Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
Text:
{text}
"""


################################################################################
# Drought Response Parsers
################################################################################

DROUGHT_RESPONSE_PARSER_EN = """
Extract whether the following text is related to climate drought.
Format instructions:
{format_instructions}
Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
Text:
{text}
"""


################################################################################
# Impact Response Parsers
################################################################################

IMPACT_RESPONSE_PARSER_EN = """
Extract whether the following text mentions an impact of climate drought on {impact}.
Focus solely on the impact of the drought on {impact} as mentioned in the text.
Format instructions:
{format_instructions}
Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
Text:
{text}
"""


################################################################################
# Location Response Parsers
################################################################################

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

################################################################################
# Summarization
################################################################################
SUMMARIZATION_ES = """
Resume el siguiente artículo, centrándote en los aspectos más relevantes relacionados con la sequía climática, los impactos de la sequía y sólo de la sequía y las localizaciones afectadas.
Si el artículo no menciona la sequía climática, el resumen únicamente debe indicar explícitamente que no se menciona la sequía climática ni ningún impacto relacionado.
Texto:
{text}
"""

SUMMARIZATION_EN = """
Summarize the following article, focusing on the most relevant aspects related to climate drought, the impacts of drought, and only drought, and the affected locations.
If the article does not mention climate drought, the summary should explicitly state that climate drought or any related impact is not mentioned.
Text:
{text}
"""


class PromptTemplateManager:
    def __init__(self):
        self.templates = {
            ("drought", "classification", "boolean", "es", "text"): {
                "template": DROUGHT_CLASSIFICATION_BOOLEAN_ES,
                "variables": ["text"],
            },
            ("drought", "classification", "boolean", "en", "text"): {
                "template": DROUGHT_CLASSIFICATION_BOOLEAN_EN,
                "variables": ["text"],
            },
            ("drought", "classification", DEFAULT, "es", "text"): {
                "template": DROUGHT_CLASSIFICATION_ES,
                "variables": ["text"],
            },
            ("drought", "classification", DEFAULT, "en", "text"): {
                "template": DROUGHT_CLASSIFICATION_EN,
                "variables": ["text"],
            },
            ("drought", "response_parser", DEFAULT, "en", "json"): {
                "template": DROUGHT_RESPONSE_PARSER_EN,
                "variables": ["text"],
                "partial_variables": ["format_instructions"],
            },
            ("impact", "classification", "boolean", "es", "text"): {
                "template": IMPACT_CLASSIFICATION_BOOLEAN_ES,
                "variables": ["text", "impact"],
            },
            ("impact", "classification", "boolean", "en", "text"): {
                "template": IMPACT_CLASSIFICATION_BOOLEAN_EN,
                "variables": ["text", "impact"],
            },
            ("impact", "classification", DEFAULT, "es", "text"): {
                "template": IMPACT_CLASSIFICATION_ES,
                "variables": ["text", "impact"],
            },
            ("impact", "classification", DEFAULT, "en", "text"): {
                "template": IMPACT_CLASSIFICATION_EN,
                "variables": ["text", "impact"],
            },
            ("impact", "classification", "description", "en", "text"): {
                "template": IMPACT_CLASSIFICATION_DESCRIPTION_EN,
                "variables": ["text", "impact", "impact_description"],
            },
            ("impact", "classification", "parser_description", "en", "json"): {
                "template": IMPACT_CLASSIFICATION_JSON_DESCRIPTION_EN,
                "variables": ["text", "impact", "impact_description"],
            },
            ("impact", "classification", "parser_description", "es", "json"): {
                "template": IMPACT_CLASSIFICATION_JSON_DESCRIPTION_ES,
                "variables": ["text", "impact", "impact_description"],
            },
            ("impact", "extraction", DEFAULT, "es", "json"): {
                "template": IMPACT_EXTRACTION_JSON_ES,
                "variables": ["text", "impacts", "impact_descriptions"],
                "partial_variables": ["format_instructions"],
            },
            ("impact", "response_parser", DEFAULT, "en", "json"): {
                "template": IMPACT_RESPONSE_PARSER_EN,
                "variables": ["text", "impact"],
                "partial_variables": ["format_instructions"],
            },
            ("location", "extraction", DEFAULT, "es", "text"): {
                "template": LOCATION_EXTRACTION_ES,
                "variables": ["text"],
            },
            ("location", "extraction", DEFAULT, "en", "text"): {
                "template": LOCATION_EXTRACTION_EN,
                "variables": ["text"],
            },
            ("location", "extraction", "provinces", "en", "text"): {
                "template": LOCATION_PROVINCES_EXTRACTION_EN,
                "variables": ["text"],
            },
            ("location", "response_parser", DEFAULT, "en", "json"): {
                "template": LOCATION_RESPONSE_PARSER_EN,
                "variables": ["text"],
                "partial_variables": ["format_instructions"],
            },
            ("province", "extraction", "parser", "en", "json"): {
                "template": PROVINCES_EXTRACTION_JSON_EN,
                "variables": ["text"],
                "partial_variables": ["format_instructions"],
            },
            (DEFAULT, "response_parser", "boolean", "en", "json"): {
                "template": BOOLEAN_RESPONSE_PARSER_EN,
                "variables": ["text"],
                "partial_variables": ["format_instructions"],
            },
            (DEFAULT, "summarization", DEFAULT, "es", "text"): {
                "template": SUMMARIZATION_ES,
                "variables": ["text"],
            },
            (DEFAULT, "summarization", DEFAULT, "en", "text"): {
                "template": SUMMARIZATION_EN,
                "variables": ["text"],
            },
        }

    def get_prompt_template(
        self,
        task: str = DEFAULT,
        step: str = DEFAULT,
        category: str = DEFAULT,
        language: str = "en",
        output: str = "text",
        **kwargs,
    ) -> PromptTemplate:
        """
        Retrieves and returns a LangChain PromptTemplate for a given task, step, language, category, and output type.

        :param task: The task type (e.g., "drought", "impact", "location").
        :param step: The step within the task (e.g., "classification", "extraction").
        :param category: The category within the step (default is "default").
        :param language: The language of the template (default is "en").
        :param output: The output type of the template (default is "text").
        :param kwargs: Additional keyword arguments to format the template.
        :return: A LangChain PromptTemplate object.
        """
        try:
            template_info = self.templates[(task, step, category, language, output)]
        except KeyError:
            raise ValueError(
                f"Template for task '{task}', step '{step}', category '{category}', language '{language}', and output '{output}' not recognized."
            )

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
