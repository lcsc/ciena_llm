from pydantic import BaseModel, Field


class ImpactLLMResponse(BaseModel):
    response: bool = Field(
        description="Whether the article mentions impacts of a climatic drought on the specific impact type."
    )


# TODO this would need to pass what impact we are talking about
