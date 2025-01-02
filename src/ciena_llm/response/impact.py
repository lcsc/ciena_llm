from pydantic import BaseModel, Field, model_validator

IMPACTS = ["agriculture", "livestock", "energy", "hydrological_resources"]

# TODO parametrize for many impacts


class ImpactLLMResponse(BaseModel):

    drought: bool = Field(description="Whether the article mentions impacts of drought")

    agriculture: bool = Field(
        description="Whether the article mentions impacts on agriculture"
    )

    livestock: bool = Field(
        description="Whether the article mentions impacts on livestock"
    )

    energy: bool = Field(description="Whether the article mentions impacts on energy")

    hydrological_resources: bool = Field(
        description="Whether the article mentions impacts on hydrological resources"
    )

    @model_validator(mode="before")
    def set_defaults(cls, values):
        for field in cls.model_fields:
            if not values.get(field):
                values[field] = False
        return values
