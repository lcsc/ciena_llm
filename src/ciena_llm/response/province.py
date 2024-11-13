from pydantic import BaseModel, Field


class ProvinceLLMResponse(BaseModel):
    response: list[str] = Field(
        default_factory=list,
        description="Provinces affected by the drought as mentioned or inferred from the article.",
    )
