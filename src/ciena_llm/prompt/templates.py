################################################################################
# Summarization
################################################################################

SUMMARIZATION_ES = """
Resume el siguiente artículo.

Texto:
{text}
"""

SUMMARIZATION_EN = """
Summarize the following article.

Text:
{text}
"""

SUMMARIZATION_SPECIFIC_ES = """
Resume el siguiente artículo, centrándote en los aspectos más relevantes relacionados con la sequía, los impactos de la sequía y sólo de la sequía y las localizaciones afectadas.
Si el artículo no menciona la sequía, el resumen únicamente debe indicar explícitamente que no se menciona la sequía ni ningún impacto relacionado.

Texto:
{text}
"""

SUMMARIZATION_SPECIFIC_EN = """
Summarize the following article, focusing on the most relevant aspects related to drought, the impacts of drought, and only drought, and the affected locations.
If the article does not mention drought, the summary should explicitly state that drought or any related impact is not mentioned.

Text:
{text}
"""

################################################################################
# Self-Criticism: Self-Calibration
################################################################################

SELF_CRITICISM_ES = """
Dado el siguiente prompt:
{prompt}

Y la siguiente respuesta:
{response}

Analiza la respuesta y determina si es correcta o incorrecta.

Si es incorrecta, proporciona una breve explicación de por qué es incorrecta y la respuesta correcta.

Si es correcta, proporciona la misma respuesta correcta.
"""

SELF_CRITICISM_EN = """
Given the following prompt:
{prompt}

And the following response:
{response}

Analyze the response and determine whether it is correct or incorrect.

If it is incorrect, provide a brief explanation of why it is incorrect and the correct response.

If it is correct, provide the same correct response.
"""

################################################################################
# Event Identification (extraction)
################################################################################

EVENT_EXTRACTION_EN = """
Analyze the following article and determine if the news article mentions an event related to {event}.
Text:
{text}
"""

EVENT_EXTRACTION_ES = """
Analiza el siguiente artículo y determina si la noticia menciona un evento relacionado con {event}.
Texto:
{text}
"""


################################################################################
# Drought Impact Extraction (Multi-Impact)
################################################################################

DROUGHT_IMPACT_EXTRACTION_SIMPLE_ES = """
Eres una persona experta en análisis ambiental. Tu tarea es analizar el siguiente artículo de prensa y determinar si informa o menciona algún impacto causado por la sequía en determinados aspectos.

Los aspectos que debes considerar son:
{impacts}

Lee detenidamente el artículo y determina, para cada aspecto, si se menciona un impacto atribuido específicamente a la sequía. No infieras impactos a menos que estén claramente expresados o fuertemente implicados en el texto.

Artículo a analizar:
{text}
"""

DROUGHT_IMPACT_EXTRACTION_SIMPLE_EN = """
You are an expert in environmental analysis. Your task is to analyze the following news article and determine whether it reports or mentions any impact caused by drought on specific aspects.

The aspects to consider are: {impacts}

Please carefully read the article and determine for each aspect whether there is a reported impact caused specifically by drought. Do not infer impacts unless they are clearly stated or strongly implied in the text.

Article to analyze:
{text}
"""

DROUGHT_IMPACT_EXTRACTION_DESCRIPTION_ES = """
Eres una persona experta en análisis ambiental. Tu tarea es analizar el siguiente artículo de prensa y determinar si informa o menciona algún impacto causado por la sequía en determinados aspectos.

Los aspectos que debes considerar son:
{impacts}

Cada uno de estos aspectos se describe brevemente a continuación para orientar la interpretación, aunque estas definiciones no son exhaustivas:

{impact_descriptions}

Lee detenidamente el artículo y determina, para cada aspecto, si se menciona un impacto atribuido específicamente a la sequía. No infieras impactos a menos que estén claramente expresados o fuertemente implicados en el texto.

Artículo a analizar:
{text}
"""

DROUGHT_IMPACT_EXTRACTION_DESCRIPTION_EN = """
You are an expert in environmental analysis. Your task is to analyze the following news article and determine whether it reports or mentions any impact caused by drought on specific aspects.

The aspects to consider are: {impacts}

Each aspect is briefly described below to guide interpretation, but these definitions are not exhaustive:

{impact_descriptions}

Please carefully read the article and determine for each aspect whether there is a reported impact caused specifically by drought. Do not infer impacts unless they are clearly stated or strongly implied in the text.

Article to analyze:
{text}
"""


################################################################################
# Location Extraction
################################################################################

DROUGHT_LOCATION_EXTRACTION_ES = """
Analiza el siguiente artículo relacionado con la sequía. Determina las localizaciones que aparecen en el texto que impactadas por la sequía. Además, indica a que tipo de localización se refiere (e.g. municipio, provincia, comunidad autonoma, río, presa, cuenca, etc.). Lista únicamente aquellas que estén directamente relacionadas con la sequía. Por localización, indica una pequeña descripción del impacto de la sequía en esa localización según la noticia. En el caso de que no haya ninguna localización impactada por la sequía, no menciones ninguna.

Texto:
{text}
"""

DROUGHT_LOCATION_EXTRACTION_EN = """
Analyze the following article related to drought.
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

DROUGHT_LOCATION_PROVINCE_EXTRACTION_EN = """
Analyze the following news article related to drought.
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
# Drought Provinces Extraction
################################################################################

DROUGHT_PROVINCE_EXTRACTION_EN = """
Given a news article describing drought impacts in Spanish regions, return the list of affected provinces.
Identify provinces explicitly mentioned or infer them from the described locations.
If you cannot identify specific provinces, return all provinces in the regions mentioned.
Note that the text may refer to autonomous communities or specific cities, towns, and municipalities, which are not the provinces being requested. Do not include these autonomous communities or municipalities in the output.
Return the province names in Spanish.

Text:
{text}
"""


DROUGHT_PROVINCE_EXTRACTION_ES = """
Dado un artículo de noticias que describe los impactos de la sequía en regiones españolas, devuelve la lista de provincias afectadas.
Identifica las provincias mencionadas explícitamente o infiérelas de las localizaciones descritas.
Si no puedes identificar provincias específicas, devuelve todas las provincias en las regiones mencionadas.
Ten en cuenta que el texto puede referirse a comunidades autónomas o ciudades, pueblos y municipios específicos, que no son las provincias solicitadas. No incluyas estas comunidades autónomas o municipios en la salida.
Devuelve los nombres de las provincias en español.

Texto:
{text}
"""


################################################################################
# Hail Event Extraction
################################################################################

HAIL_EVENT_EXTRACTION_EN = """
You are an expert in environmental and meteorological analysis. Your task is to thoroughly analyze the following news article and extract all information related to past hail events described in the text.

Only consider hail events that have already occurred. Do not include any information about possible or predicted hail events.

For each past hail event mentioned or clearly implied, provide a summary with the following details for each event:

- locations (list[str]): List all specific locations (e.g., cities, towns, regions, landmarks) directly affected by the hail event. Use proper names without additional descriptive text. If no locations are mentioned, leave this field empty.
- date (str): The date and, if available, the time when the hail event occurred. Use the format YYYY-MM-DD for dates, and YYYY-MM-DD HH:mm if a specific time is provided or can be reliably inferred. If neither date nor time can be determined, leave this field empty.
- date_text (str): If the article provides a textual description of the date or time (e.g., "last Tuesday", "in early June"), include it here using the exact wording and language from the article. If not available, leave this field empty.
- duration (str | int): The duration of the hail event in minutes if available or can be inferred. If the duration cannot be inferred, leave this field empty.
- duration_text (str): If the article provides a textual description of the duration (e.g., "a few minutes", "several hours"), include it here using the exact wording and language from the article. If not available, leave this field empty.
- damages (list[str]): List all types of damages or impacts caused specifically by this hail event, using the exact wording and language from the article whenever possible. Only include damages directly attributed to this hail event, and ensure to include quantifiable damages (such as number of affected hectares, casualties, or economic losses) if provided.
- size (str): The size of the hailstones, if mentioned, using the exact text and language from the article (e.g., in centimeters, millimeters, or using descriptive terms such as "golf ball-sized"). If not mentioned, leave this field empty.

If the article does not mention or clearly imply any past hail events, do not return any hail event information.

Text:
{text}
"""


################################################################################
# Event Identification Response Parsers
################################################################################

EVENT_IDENTIFICATION_RESPONSE_PARSING_EN = """
Extract whether the following LLM response says the article mentions an event related to {event}.
Text:
{text}
"""

EVENT_IDENTIFICATION_RESPONSE_PARSING_ES = """
Extrae si la siguiente respuesta de un LLM indica que el artículo menciona un evento relacionado con {event}.
Texto:
{text}
"""


################################################################################
# Drought Impact Response Parsers
################################################################################

DROUGHT_IMPACT_RESPONSE_PARSING_EN = """
Extract whether the following LLM response says the article mentions an impact of drought on {impacts}.

The impacts are defined as follows:
{impact_descriptions}

Text:
{text}
"""

DROUGHT_IMPACT_RESPONSE_PARSING_ES = """
Extrae si la siguiente respuesta de un LLM indica que el artículo menciona un impacto de la sequía en {impacts}.

Los impactos se definen de la siguiente manera:
{impact_descriptions}

Texto:
{text}
"""

################################################################################
# Location Response Parsers
################################################################################

LOCATION_RESPONSE_PARSING_EN = """
Extract from the following LLM response the locations.

Text:
{text}
"""

################################################################################
# Province Response Parsers
################################################################################

PROVINCE_RESPONSE_PARSING_EN = """
Extract from the following LLM response the provinces.

If other locations are mentioned, infer the provinces.

Text:
{text}
"""

PROVINCE_RESPONSE_PARSING_ES = """
Extrae de la siguiente respuesta de un LLM las provincias.

Si se mencionan otras localizaciones, infiere las provincias.

Texto:
{text}
"""

################################################################################
# Hail Event Response Parsers
################################################################################

HAIL_EVENT_RESPONSE_PARSING_EN = """
Extract from the following LLM response the hail events information.

If no hail event is mentioned, do not return any event.

Text:
{text}
"""


################################################################################
# Drough Classification
################################################################################

# DROUGHT_CLASSIFICATION_BOOLEAN_ES = """
# Analiza el siguiente artículo y determina si la noticia está relacionada con la sequía.

# Por ejemplo, si el artículo está relacionado con la sequía, responde únicamente la palabra "True" y si no lo está, responde "False". No añadas ningún signo de puntuación ni proporciones ninguna explicación adicional. Sólo True/False.

# Texto:
# {text}
# """

# DROUGHT_CLASSIFICATION_BOOLEAN_EN = """
# Analyze the following article and determine if the news article is mentions the existance of drought.
# In your response, provide only an affirmative or negative answer.

# Text:
# {text}
# """

# DROUGHT_CLASSIFICATION_ES = """
# Analiza el siguiente artículo y determina si la noticia está relacionada con la sequía.

# Texto:
# {text}
# """

# DROUGHT_CLASSIFICATION_EN = """
# Analyze the following article and determine if the news article is mentions the existance of drought.

# Text:
# {text}
# """


################################################################################
# Drought Impact Classification (Single Impact)
################################################################################

# DROUGHT_IMPACT_CLASSIFICATION_BOOLEAN_ES = """
# Analiza el siguiente artículo relacionado con la sequía. Determina si esta noticia menciona un impacto de la sequía en {impact}.

# Por ejemplo, si el artículo menciona un impacto en {impact}, responde únicamente la palabra "True" y si no lo está, responde "False". No añadas ningún signo de puntuación ni proporciones ninguna explicación adicional. Sólo True/False.

# Texto:
# {text}
# """

# DROUGHT_IMPACT_CLASSIFICATION_BOOLEAN_EN = """
# Analyze the following article related to drought. Determine whether the news article mentions an impact of drought on {impact}.
# In your response, focus solely on the impact of the drought on {impact} as mentioned in the article.
# In your response, provide only an affirmative or negative answer.

# Text:
# {text}
# """

# DROUGHT_IMPACT_CLASSIFICATION_ES = """
# Analiza el siguiente artículo relacionado con la sequía. Determina si esta noticia menciona un impacto de la sequía en {impact}.

# Texto:
# {text}
# """

# DROUGHT_IMPACT_CLASSIFICATION_EN = """
# Analyze the following article related to drought. Determine whether the news article mentions an impact of drought on {impact}.
# In your response, focus solely on the impact of the drought on {impact} as mentioned in the article.

# Text:
# {text}
# """

# DROUGHT_IMPACT_CLASSIFICATION_DESCRIPTION_EN = """
# Analyze the following article related to drought. Determine whether the news article mentions an impact of drought on {impact}.
# In your response, focus solely on the impact of the drought on {impact} as mentioned in the article.

# The impact is defined as follows:
# {impact_description}

# Text:
# {text}
# """

# DROUGHT_IMPACT_CLASSIFICATION_DESCRIPTION_ES = """
# Analiza el siguiente artículo relacionado con la sequía. Determina si esta noticia menciona un impacto de la sequía en {impact}.
# En tu respuesta, enfócate únicamente en el impacto de la sequía en {impact} tal como se menciona en el artículo.

# El impacto se define como sigue:
# {impact_description}

# Texto:
# {text}
# """


################################################################################
# Boolean Response Parsers
################################################################################

# BOOLEAN_RESPONSE_PARSING_EN = """
# Extract whether the following LLM response is affirmative or negative.

# Text:
# {text}
# """


################################################################################
# Drought Response Parsers
################################################################################

# DROUGHT_RESPONSE_PARSING_EN = """
# Extract whether the following LLM response says the article is related to drought.

# Text:
# {text}
# """


# Format instructions:
# {format_instructions}
# Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).

# Instrucciones de formato:
# {format_instructions}
# Proporciona únicamente el JSON dentro de un bloque de código de markdown (sin resaltado de sintaxis y sin texto adicional alrededor).

# Format instructions:
# {format_instructions}
# For each location, include all properties as specified in the schema, including optional ones, if they appear in the text.
# If there are no locations impacted by the drought, provide an empty JSON object.
# Return only the JSON inside a markdown fenced code block (without syntax highlighting and no additional text around it).
# Do not encode any special characters and do not use any Unicode escape sequences in the output.

# Provide the only response in the following format:
# Format instructions:
# ```json
# {{"response": true or false}}
# ```

# Proporciona la única respuesta en el siguiente formato:
# Instrucciones de formato:
# ```json
# {{"response": true or false}}
# ```

# Output the list as parsable JSON with the following structure.
# {"provinces":[]}
# Do not output anything else but the list of provinces.
