from langchain_core.prompts import PromptTemplate
from prompts import *


class PromptTemplateManager:
    def __init__(self):
        self.templates = {
            "drought_classification_boolean_es": {
                "template": DROUGHT_CLASSIFICATION_BOOLEAN_ES,
                "variables": ["text"],
            },
            "drought_classification_boolean_en": {
                "template": DROUGHT_CLASSIFICATION_BOOLEAN_EN,
                "variables": ["text"],
            },
            "drought_classification_es": {
                "template": DROUGHT_CLASSIFICATION_ES,
                "variables": ["text"],
            },
            "drought_classification_en": {
                "template": DROUGHT_CLASSIFICATION_EN,
                "variables": ["text"],
            },
            "impact_classification_boolean_es": {
                "template": IMPACT_CLASSIFICATION_BOOLEAN_ES,
                "variables": ["text"],
            },
            "impact_classification_boolean_en": {
                "template": IMPACT_CLASSIFICATION_BOOLEAN_EN,
                "variables": ["text"],
            },
            "impact_classification_es": {
                "template": IMPACT_CLASSIFICATION_ES,
                "variables": ["text", "impact"],
            },
            "impact_classification_en": {
                "template": IMPACT_CLASSIFICATION_EN,
                "variables": ["text", "impact"],
            },
            "impact_classification_description_en": {
                "template": IMPACT_CLASSIFICATION_DESCRIPTION_EN,
                "variables": ["text", "impact", "impact_description"],
            },
            "impact_classification_parser_description_en": {
                "template": IMPACT_CLASSIFICATION_PARSER_DESCRIPTION_EN,
                "variables": ["text", "impact", "impact_description"],
                # "partial_variables": ["format_instructions"],
            },
            "impact_classification_parser_description_es": {
                "template": IMPACT_CLASSIFICATION_PARSER_DESCRIPTION_ES,
                "variables": ["text", "impact", "impact_description"],
                # "partial_variables": ["format_instructions"],
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
            "provinces_extraction_parser_en": {
                "template": PROVINCES_EXTRACTION_PARSER_EN,
                "variables": ["text"],
                "partial_variables": ["format_instructions"],
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
