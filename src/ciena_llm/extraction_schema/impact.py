from typing import Optional

from pydantic import BaseModel, Field, create_model

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
ImpactExtractionSchema: BaseModel = create_model("ImpactExtractionSchema", **fields)


@classmethod
def default_response(cls):
    """
    Get the default response for the model
    """
    return {"drought": None, **{impact: None for impact in IMPACTS}}


@classmethod
def format_instructions_as_json(cls):
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


ImpactExtractionSchema.default_response = default_response
ImpactExtractionSchema.format_instructions_as_json = format_instructions_as_json
