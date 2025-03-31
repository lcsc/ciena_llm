from typing import Type

from pydantic import BaseModel, Field, create_model


def build_model(event: str) -> Type[BaseModel]:
    """
    Factory function to create a dynamic ProvinceLLMResponse model.

    :param event: The event name
    :return: A dynamically created Pydantic model
    """

    fields = {
        "response": (
            list[str],
            Field(
                default_factory=list,
                description=f"Provinces affected by {event} as mentioned or inferred from the article.",
            ),
        )
    }

    # Dynamically create model
    province_extraction_schema: BaseModel = create_model(
        "ProvinceExtractionSchema", **fields
    )

    @classmethod
    def normalize_response_format(cls, response):
        """
        Parser to ensure the response is always a dictionary

        Convert the response to a dictionary if it is a list.
        This handles common generation errors in the LLM when no provinces are found.
        """

        # If is a list, return it as a dictionary
        if isinstance(response, list):
            return {"response": response}

        # If is not a dictionary, return an empty dictionary
        if not isinstance(response, dict):
            return {"response": []}

        # Else return the response as is
        return response

    @classmethod
    def default_response(cls):
        """
        Get the default response for the model
        """
        default_values = {"response": []}
        return cls(**default_values)

    @classmethod
    def format_instructions_as_json(cls):
        """
        Get the JSON format instructions for the model
        """
        # TODO maybe put this in the prompt template manager?
        # JSON format instructions for the model
        return """
```json 
{
    "response": [
        <province>,
        ...
    ]
}
```
"""

    # Add the class methods to the model
    province_extraction_schema.normalize_response_format = normalize_response_format
    province_extraction_schema.default_response = default_response
    province_extraction_schema.format_instructions_as_json = format_instructions_as_json

    return province_extraction_schema
