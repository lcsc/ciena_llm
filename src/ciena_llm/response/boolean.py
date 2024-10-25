from pydantic import BaseModel, Field


class BooleanLLMResponse(BaseModel):
    response: bool = Field(description="Whether the reponse is affirmative or negative.")
