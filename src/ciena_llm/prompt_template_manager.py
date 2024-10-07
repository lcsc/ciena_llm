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
Analyze the following article and determine if the news is related to climate drought.
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
Analyze the following article related to climate drought. Determine if this news mentions an impact of the drought on {impact}.
Text:
{text}
"""

LOCATION_EXTRACTION_ES = """
Analiza el siguiente artículo relacionado con la sequía climática. Determina las localizaciones que aparecen en el texto que impactadas por la sequía. Además, indica a que tipo de localización se refiere (e.g. municipio, provincia, comunidad autonoma, río, presa, cuenca, etc.). Lista únicamente aquellas que estén directamente relacionadas con la sequía. Por localización, indica una pequeña descripción del impacto de la sequía en esa localización según la noticia. En el caso de que no haya ninguna localización impactada por la sequía, no menciones ninguna.
Texto:
{text}
"""

LOCATION_EXTRACTION_EN = """
Analyze the following article related to climate drought. Determine the locations mentioned in the text that are impacted by the drought. Additionally, indicate the type of location (e.g., municipality, province, autonomous community, river, dam, basin, etc.). List only those that are directly related to the drought. For each location, provide a brief description of the drought's impact on that location according to the news. If there are no locations impacted by the drought, do not mention any.
Text:
{text}
"""

DROUGHT_RESPONSE_PARSER_EN = """
Extract whether the following text is related to climate drought.
{format_instructions}
Text:
{text}
"""

IMPACT_RESPONSE_PARSER_EN = """
# TODO
"""

LOCATION_RESPONSE_PARSER_EN = """
Extract the locations impacted by climate drought from the following text.
{format_instructions}
If there are no locations impacted by climate drought, provide an empty JSON object.
Only provide the JSON between a markdown fenced code block without syntax highlighting and no other text around it.
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
