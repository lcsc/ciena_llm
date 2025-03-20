from pydantic import BaseModel, Field, create_model, model_validator
from typing import Optional

# TEST

# TODO get from config
IMPACTS = ["agriculture", "livestock", "energy", "hydrological_resources"]

# Dynamically create fields for the model
fields = {
    impact: (
        Optional[bool],
        Field(
            description=f"Whether the article mentions impacts on {impact.replace('_', ' ')}"
        ),
    )
    for impact in IMPACTS
}

# Add the drought field separately
fields["drought"] = (
    Optional[bool],
    Field(description="Whether the article mentions impacts of drought"),
)

# Create the model dynamically
ImpactLLMResponse: BaseModel = create_model("ImpactLLMResponse", **fields)


@classmethod
def get_default_response(cls):
    """
    Get the default response for the model
    """
    return {"drought": None, **{impact: None for impact in IMPACTS}}


@classmethod
def get_format_instructions(cls):
    """
    Get the JSON format instructions for the model
    """
    # JSON format instructions for the model
    impacts_json = ",\n    ".join([f'"{i}": <true or false>' for i in IMPACTS])

    return f"""
```json
{{
    "drought": <true or false>,
    {impacts_json}
}}
```
"""


ImpactLLMResponse.get_default_response = get_default_response
ImpactLLMResponse.get_format_instructions = get_format_instructions
