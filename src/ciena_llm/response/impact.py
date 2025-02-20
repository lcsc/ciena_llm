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
    return {"drought": None, **{impact: None for impact in IMPACTS}}


@classmethod
def get_format_instructions(cls):
    # TODO maybe put this in the prompt template manager?
    # JSON format instructions for the model
    return f"""
```json 
{{
    "drought": <true or false>,
    {"\n\t".join([f"\"{i}\": <true or false>," for i in IMPACTS])}
}}
```
"""


ImpactLLMResponse.get_default_response = get_default_response
ImpactLLMResponse.get_format_instructions = get_format_instructions
