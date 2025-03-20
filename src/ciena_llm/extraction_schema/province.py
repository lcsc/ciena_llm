from pydantic import BaseModel, Field


class ProvinceExtractionSchema(BaseModel):
    response: list[str] = Field(
        default_factory=list,
        description="Provinces affected by the drought as mentioned or inferred from the article.",
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
        return {"response": []}

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
