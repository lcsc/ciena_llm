from typing import Dict

from langchain_core.prompts import PromptTemplate

from ciena_llm.prompt.templates import *


DEFAULT = None


class PromptTemplateManager:
    TEMPLATES = {
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
        ("drought", "response_parsing", DEFAULT, "en", "json"): {
            "template": DROUGHT_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        ("impact_extraction", "classification", "boolean", "es", "text"): {
            "template": IMPACT_CLASSIFICATION_BOOLEAN_ES,
            "variables": ["text"],
            "partial_variables": ["impact"],
        },
        ("impact_extraction", "classification", "boolean", "en", "text"): {
            "template": IMPACT_CLASSIFICATION_BOOLEAN_EN,
            "variables": ["text"],
            "partial_variables": ["impact"],
        },
        ("impact_extraction", "classification", DEFAULT, "es", "text"): {
            "template": IMPACT_CLASSIFICATION_ES,
            "variables": ["text"],
            "partial_variables": ["impact"],
        },
        ("impact_extraction", "classification", DEFAULT, "en", "text"): {
            "template": IMPACT_CLASSIFICATION_EN,
            "variables": ["text"],
            "partial_variables": ["impact"],
        },
        ("impact_extraction", "classification", "description", "en", "text"): {
            "template": IMPACT_CLASSIFICATION_DESCRIPTION_EN,
            "variables": ["text"],
            "partial_variables": ["impact", "impact_description"],
        },
        ("impact_extraction", "classification", "parser_description", "en", "json"): {
            "template": IMPACT_CLASSIFICATION_JSON_DESCRIPTION_EN,
            "variables": ["text"],
            "partial_variables": ["impact", "impact_description"],
        },
        ("impact_extraction", "classification", "parser_description", "es", "json"): {
            "template": IMPACT_CLASSIFICATION_JSON_DESCRIPTION_ES,
            "variables": ["text"],
            "partial_variables": ["impact", "impact_description"],
        },
        ("impact_extraction", "multi_classification", "description", "es", "json"): {
            "template": IMPACT_MULTI_CLASSIFICATION_JSON_DESCRIPTION_ES,
            "variables": ["text"],
            "partial_variables": [
                "format_instructions",
                "impacts",
                "impact_descriptions",
            ],
        },
        ("impact_extraction", "multi_classification", "description", "es", "text"): {
            "template": IMPACT_MULTI_CLASSIFICATION_DESCRIPTION_ES,
            "variables": ["text"],
            "partial_variables": ["impacts", "impact_descriptions"],
        },
        ("impact_extraction", "multi_classification", "description", "en", "json"): {
            "template": IMPACT_MULTI_CLASSIFICATION_JSON_DESCRIPTION_EN,
            "variables": ["text"],
            "partial_variables": [
                "format_instructions",
                "impacts",
                "impact_descriptions",
            ],
        },
        ("impact_extraction", "multi_classification", "description", "en", "text"): {
            "template": IMPACT_MULTI_CLASSIFICATION_DESCRIPTION_EN,
            "variables": ["text"],
            "partial_variables": ["impacts", "impact_descriptions"],
        },
        ("impact_extraction", "response_parsing", DEFAULT, "en", "json"): {
            "template": IMPACT_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": [
                "format_instructions",
                "impacts",
                "impact_descriptions",
            ],
        },
        ("impact_extraction", "response_parsing", DEFAULT, "es", "json"): {
            "template": IMPACT_RESPONSE_PARSING_ES,
            "variables": ["text"],
            "partial_variables": [
                "format_instructions",
                "impacts",
                "impact_descriptions",
            ],
        },
        # ("impact_extraction", "response_parsing", DEFAULT, "es", "json"): {
        #     "template": IMPACT_RESPONSE_PARSING_ES,
        #     "variables": ["text"],
        #     "partial_variables": ["format_instructions", "impact"],
        # },
        ("location", "extraction", DEFAULT, "es", "text"): {
            "template": LOCATION_EXTRACTION_ES,
            "variables": ["text"],
        },
        ("location", "extraction", DEFAULT, "en", "text"): {
            "template": LOCATION_EXTRACTION_EN,
            "variables": ["text"],
        },
        ("location", "extraction", "provinces", "en", "text"): {
            "template": LOCATION_PROVINCE_EXTRACTION_EN,
            "variables": ["text"],
        },
        ("location", "response_parsing", DEFAULT, "en", "json"): {
            "template": LOCATION_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        ("location_extraction", "extraction", DEFAULT, "en", "json"): {
            "template": PROVINCE_EXTRACTION_JSON_EN,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        ("location_extraction", "extraction", DEFAULT, "en", "text"): {
            "template": PROVINCE_EXTRACTION_TEXT_EN,
            "variables": ["text"],
        },
        ("location_extraction", "extraction", DEFAULT, "es", "json"): {
            "template": PROVINCE_EXTRACTION_JSON_ES,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        ("location_extraction", "extraction", DEFAULT, "es", "text"): {
            "template": PROVINCE_EXTRACTION_TEXT_ES,
            "variables": ["text"],
        },
        ("location_extraction", "response_parsing", DEFAULT, "en", "json"): {
            "template": PROVINCE_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        ("location_extraction", "response_parsing", DEFAULT, "es", "json"): {
            "template": PROVINCE_RESPONSE_PARSING_ES,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        (DEFAULT, "response_parsing", "boolean", "en", "json"): {
            "template": BOOLEAN_RESPONSE_PARSING_EN,
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

    @classmethod
    def get_prompt_template(
        cls,
        task: str = DEFAULT,
        category: str = DEFAULT,
        subcategory: str = DEFAULT,
        language: str = "en",
        output: str = "text",
        **kwargs,
    ) -> PromptTemplate:
        """
        Retrieves and returns a LangChain PromptTemplate for a given task, category, language, subcategory, and output type.

        :param task: The task type (e.g., "drought", "impact", "location").
        :param category: The category within the task (e.g., "classification", "extraction").
        :param subcategory: The category within the subcategory (default is "default").
        :param language: The language of the template (default is "en").
        :param output: The output type of the template (default is "text").
        :param kwargs: Additional keyword arguments to format the template.
        :return: A LangChain PromptTemplate object.
        """
        try:
            template_info = cls.TEMPLATES[
                (task, category, subcategory, language, output)
            ]
        except KeyError:
            raise ValueError(
                f"Template for task '{task}', category '{category}', subcategory '{subcategory}', language '{language}', and output '{output}' not recognized."
            )

        template_str = template_info["template"]

        # Separate partial variables from input variables
        partial_vars = {
            k: v
            for k, v in kwargs.items()
            if k in template_info.get("partial_variables", [])
        }

        return PromptTemplate(
            template=template_str,
            input_variables=template_info["variables"],
            partial_variables=partial_vars,
        )

    @classmethod
    def get_impact_names_text(cls, impact_config: Dict, language: str) -> str:
        """
        Retrieves and returns a string of impact names from the given impacts configuration.

        :param impact_config: A dictionary of impact names and descriptions.
        :param language: The language of the impact names text.
        :return: A string of impact names.
        """
        impact_names = [i[f"text_{language}"] for i in impact_config]
        impact_names_text = ", ".join(impact_names)

        return impact_names_text

    @classmethod
    def get_impact_descriptions_text(cls, impact_config: Dict, language: str) -> str:
        """
        Retrieves and returns a string of impact descriptions from the given impacts configuration.

        :param impact_config: A dictionary of impact names and descriptions.
        :param language: The language of the impact descriptions text.
        :return: A string of impact descriptions.
        """

        impact_names = [i[f"text_{language}"] for i in impact_config]
        impact_descriptions = [i[f"description_{language}"] for i in impact_config]
        impact_descriptions_text = ", ".join(
            [
                f"{impact}: {description}"
                for impact, description in zip(impact_names, impact_descriptions)
            ]
        )

        return impact_descriptions_text
