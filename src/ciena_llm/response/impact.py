from pydantic import BaseModel, Field


class ImpactLLMResponse(BaseModel):
    impact: bool = Field(
        description="Whether the article mentions impacts of a climatic drought."
    )


# TODO this would need to pass what impact we are talking about
