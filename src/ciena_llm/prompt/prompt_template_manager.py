from typing import Dict

from langchain_core.prompts import PromptTemplate

from ciena_llm.prompt.templates import *


DEFAULT = None

FORMAT_INSTRUCTIONS_STR = {
    "es": """
Instrucciones de formato:
{format_instructions}
Asegurate que incluyes un único JSON en tu respuesta en vez de varios JSONs.
""",
    "en": """
Format instructions:
{format_instructions}
Make sure to include a single JSON in your response instead of multiple JSONs.
""",
}

COT_INSTRUCTIONS_STR = {
    "es": """
Razona paso a paso y explica tu razonamiento antes de dar la respuesta final.
""",
    "en": """
Reason step by step and explain your reasoning before giving the final answer.
""",
}


class PromptTemplateManager:
    TEMPLATES = {
        (DEFAULT, "summarization", DEFAULT, "es"): {
            "template": SUMMARIZATION_ES,
            "variables": ["text"],
        },
        (DEFAULT, "summarization", DEFAULT, "en"): {
            "template": SUMMARIZATION_EN,
            "variables": ["text"],
        },
        (DEFAULT, "self_criticism", DEFAULT, "es"): {
            "template": SELF_CRITICISM_ES,
            "variables": ["prompt", "response"],
        },
        (DEFAULT, "self_criticism", DEFAULT, "en"): {
            "template": SELF_CRITICISM_EN,
            "variables": ["prompt", "response"],
        },
        ("event", "extraction", DEFAULT, "es"): {
            "template": EVENT_EXTRACTION_ES,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("event", "extraction", DEFAULT, "en"): {
            "template": EVENT_EXTRACTION_EN,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("event", "response_parsing", DEFAULT, "es"): {
            "template": EVENT_IDENTIFICATION_RESPONSE_PARSING_ES,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("event", "response_parsing", DEFAULT, "en"): {
            "template": EVENT_IDENTIFICATION_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("impact", "extraction", "simple", "es"): {
            "template": IMPACT_EXTRACTION_SIMPLE_ES,
            "variables": ["text"],
            "partial_variables": ["event", "impacts"],
        },
        ("impact", "extraction", "simple", "en"): {
            "template": IMPACT_EXTRACTION_SIMPLE_EN,
            "variables": ["text"],
            "partial_variables": ["event", "impacts"],
        },
        ("impact", "extraction", "description", "es"): {
            "template": IMPACT_EXTRACTION_DESCRIPTION_ES,
            "variables": ["text"],
            "partial_variables": ["event", "impacts", "impact_descriptions"],
        },
        ("impact", "extraction", "description", "en"): {
            "template": IMPACT_EXTRACTION_DESCRIPTION_EN,
            "variables": ["text"],
            "partial_variables": ["event", "impacts", "impact_descriptions"],
        },
        ("impact", "response_parsing", DEFAULT, "en"): {
            "template": IMPACT_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["event", "impacts", "impact_descriptions"],
        },
        ("impact", "response_parsing", DEFAULT, "es"): {
            "template": IMPACT_RESPONSE_PARSING_ES,
            "variables": ["text"],
            "partial_variables": ["event", "impacts", "impact_descriptions"],
        },
        ("location", "extraction", "location", "es"): {
            "template": LOCATION_EXTRACTION_ES,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("location", "extraction", "location", "en"): {
            "template": LOCATION_PROVINCE_EXTRACTION_EN,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("location", "response_parsing", "location", "en"): {
            "template": LOCATION_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("location", "extraction", "province", "en"): {
            "template": PROVINCE_EXTRACTION_EN,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("location", "extraction", "province", "es"): {
            "template": PROVINCE_EXTRACTION_ES,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("location", "response_parsing", "province", "en"): {
            "template": PROVINCE_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("location", "response_parsing", "province", "es"): {
            "template": PROVINCE_RESPONSE_PARSING_ES,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("hail_event", "extraction", DEFAULT, "en"): {
            "template": HAIL_EVENT_EXTRACTION_EN,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
        ("hail_event", "response_parsing", DEFAULT, "en"): {
            "template": HAIL_EVENT_RESPONSE_PARSING_EN,
            "variables": ["text"],
            "partial_variables": ["event"],
        },
    }

    @classmethod
    def get_prompt_template(
        cls,
        extraction_task: str = DEFAULT,
        step: str = DEFAULT,
        category: str = DEFAULT,
        language: str = "en",
        cot: bool = False,
        output: str = "text",
        **kwargs,
    ) -> PromptTemplate:
        """
        Retrieves and returns a LangChain PromptTemplate for a given extraction_task, step, language, category, and output type.

        :param extraction_task: The extraction_task
        :param step: The pipeline step (e.g., "classification", "extraction").
        :param category: The step within the category (default is "default").
        :param language: The language of the template (default is "en").
        :param output: The output type of the template (default is "text"). Options are "text" and "json". If "json", the format instructions will be appended to the template.
        :param kwargs: Additional keyword arguments to format the template.
        :return: A LangChain PromptTemplate object.
        """
        try:
            template_info = cls.TEMPLATES[(extraction_task, step, category, language)]
        except KeyError as exc:
            raise ValueError(
                f"Template for extraction_task '{extraction_task}', step '{step}', category '{category}', and language '{language}' not recognized."
            ) from exc

        template_str = template_info["template"]

        if cot:
            template_str = f"{template_str}\n\n{COT_INSTRUCTIONS_STR[language]}"

        # If output is JSON, append the format instructions to the template
        if output == "json":
            template_str = f"{template_str}\n\n{FORMAT_INSTRUCTIONS_STR[language]}"
            if "partial_variables" not in template_info:
                template_info["partial_variables"] = []
            template_info["partial_variables"].append("format_instructions")

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
    def get_event_name_text(cls, event_config: Dict, language: str) -> str:
        """
        Retrieves and returns a string of event names from the given event configuration.

        :param event_config: A dictionary of event names and descriptions.
        :param language: The language of the event names text.
        :return: A string of event names.
        """
        if not event_config:
            return None
        event_name = event_config[f"text_{language}"]

        return event_name

    @classmethod
    def get_impact_names_text(cls, impact_config: Dict, language: str) -> str:
        """
        Retrieves and returns a string of impact names from the given impacts configuration.

        :param impact_config: A dictionary of impact names and descriptions.
        :param language: The language of the impact names text.
        :return: A string of impact names.
        """
        if not impact_config:
            return None
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

        if not impact_config:
            return None

        impact_names = [i[f"text_{language}"] for i in impact_config]
        impact_descriptions = [i[f"description_{language}"] for i in impact_config]
        impact_descriptions_text = ", ".join(
            [
                f"{impact}: {description}"
                for impact, description in zip(impact_names, impact_descriptions)
            ]
        )

        return impact_descriptions_text
