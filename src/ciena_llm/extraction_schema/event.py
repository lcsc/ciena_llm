from typing import Type, Optional

from pydantic import BaseModel, Field, create_model


def build_model(event: str) -> Type[BaseModel]:
    """
    Factory function to create a dynamic EventLLMResponse model.

    :param event: The event name
    :return: A dynamically created Pydantic model
    """

    # Dynamically create fields for the model
    fields = {}

    # Add the event field
    fields[event] = (
        Optional[bool],
        Field(
            description=f"Whether the article mentions the event of {event}",
            default=False,
        ),
    )

    # Dynamically create model
    event_extraction_schema: BaseModel = create_model("EventLLMResponse", **fields)

    @classmethod
    def default_response(cls):
        """
        Get the default response for the model
        """
        default_values = {event: None}
        return cls(**default_values)

    @classmethod
    def format_instructions_as_json(cls):
        """
        Get the JSON format instructions for the model
        """
        return f"""
```json
{{
    "{event}": <true or false>
}}
```
"""

    # Add the class methods to the model
    event_extraction_schema.default_response = default_response
    event_extraction_schema.format_instructions_as_json = format_instructions_as_json

    return event_extraction_schema
