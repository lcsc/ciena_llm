from pydantic import BaseModel, Field


class DroughtLLMResponse(BaseModel):
    drought: bool = Field(
        description="Whether the article mentions impacts of a climatic drought."
    )
