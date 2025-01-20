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
        ("impact", "multi_classification", "description", "es", "json"): {
            "template": IMPACT_MULTI_CLASSIFICATION_JSON_DESCRIPTION_ES,
            "variables": ["text", "impacts", "impact_descriptions"],
            "partial_variables": ["format_instructions"],
        },
        ("impact", "multi_classification", "description", "es", "text"): {
            "template": IMPACT_MULTI_CLASSIFICATION_DESCRIPTION_ES,
            "variables": ["text", "impacts", "impact_descriptions"],
        },
        ("impact", "multi_classification", "description", "en", "json"): {
            "template": IMPACT_MULTI_CLASSIFICATION_JSON_DESCRIPTION_EN,
            "variables": ["text", "impacts", "impact_descriptions"],
            "partial_variables": ["format_instructions"],
        },
        ("impact", "multi_classification", "description", "en", "text"): {
            "template": IMPACT_MULTI_CLASSIFICATION_DESCRIPTION_EN,
            "variables": ["text", "impacts", "impact_descriptions"],
        },
        ("impact", "response_parsing", DEFAULT, "en", "json"): {
            "template": IMPACT_RESPONSE_PARSING_EN,
            "variables": ["text", "impacts", "impact_descriptions"],
            "partial_variables": ["format_instructions"],
        },
        ("impact", "response_parsing", DEFAULT, "es", "json"): {
            "template": IMPACT_RESPONSE_PARSING_ES,
            "variables": ["text", "impacts", "impact_descriptions"],
            "partial_variables": ["format_instructions"],
        },
        ("impact", "response_parsing", DEFAULT, "es", "json"): {
            "template": IMPACT_RESPONSE_PARSING_ES,
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
            "template": LOCATION_PROVINCE_EXTRACTION_EN,
            "variables": ["text"],
        },
        ("location", "response_parsing", DEFAULT, "en", "json"): {
            "template": LOCATION_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        ("province", "extraction", DEFAULT, "en", "json"): {
            "template": PROVINCE_EXTRACTION_JSON_EN,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        ("province", "extraction", DEFAULT, "en", "text"): {
            "template": PROVINCE_EXTRACTION_TEXT_EN,
            "variables": ["text"],
        },
        ("province", "extraction", DEFAULT, "es", "json"): {
            "template": PROVINCE_EXTRACTION_JSON_ES,
            "variables": ["text"],
            "partial_variables": ["format_instructions"],
        },
        ("province", "extraction", DEFAULT, "es", "text"): {
            "template": PROVINCE_EXTRACTION_TEXT_ES,
            "variables": ["text"],
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
            template_info = cls.TEMPLATES[(task, step, category, language, output)]
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
