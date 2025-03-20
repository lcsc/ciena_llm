from typing import Optional, List, Type

from pydantic import BaseModel, Field, create_model


def build_model(event: str, impacts: List[str]) -> Type[BaseModel]:
    """
    Factory function to create a dynamic ImpactLLMResponse model.

    :param event: The event name
    :param impacts: A list of impact names
    :return: A dynamically created Pydantic model
    """

    # Dynamically create fields for the model
    fields = {
        impact: (
            Optional[bool],
            Field(
                description=f"Whether the article mentions impacts on {impact.replace('_', ' ')}"
            ),
        )
        for impact in impacts
    }

    # Add the event field separately
    fields[event] = (
        Optional[bool],
        Field(description=f"Whether the article mentions impacts of {event}"),
    )

    # Dynamically create model
    impact_extraction_schema: BaseModel = create_model(
        "ImpactExtractionSchema", **fields
    )

    @classmethod
    def default_response(cls):
        """
        Get the default response for the model
        """
        return {event: None, **{impact: None for impact in impacts}}

    @classmethod
    def format_instructions_as_json(cls):
        """
        Get the JSON format instructions for the model
        """
        impacts_json = ",\n    ".join([f'"{i}": <true or false>' for i in impacts])

        return f"""
```json
{{
    {event}: <true or false>,
    {impacts_json}
}}
```
"""

    # Add the class methods to the model
    impact_extraction_schema.default_response = default_response
    impact_extraction_schema.format_instructions_as_json = format_instructions_as_json

    return impact_extraction_schema
