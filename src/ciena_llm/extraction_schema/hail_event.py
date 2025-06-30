from typing import List
from pydantic import BaseModel, Field


class HailEvent(BaseModel):
    locations: List[str] = Field(
        default_factory=list,
        description="List of locations directly affected by the hail event.",
    )
    date: str = Field(
        default="",
        description="Date of the hail event (preferred format: YYYY-MM-DD HH:mm, but other formats are allowed if cannot be inferred from text).",
    )
    duration: str = Field(
        default="",
        description="Duration of the hail event (preferred format: minutes, but can be text if cannot be inferred from text).",
    )
    damages: List[str] = Field(
        default_factory=list,
        description="List of damages caused by the hail event.",
    )
    size: str = Field(
        default="",
        description="Size of the hail.",
    )


class HailEvents(BaseModel):
    events: List[HailEvent] = Field(
        default_factory=list, description="List of hail events."
    )

    @classmethod
    def default_response(cls):
        return cls(events=[])

    @classmethod
    def format_instructions_as_json(cls):
        return (
            "```json\n"
            "{\n"
            '  "events": [\n'
            "    {\n"
            '      "locations": [<list of locations>],\n'
            '      "date": "<date string>",\n'
            '      "duration": "<duration string>",\n'
            '      "damages": [<list of damages>],\n'
            '      "size": "<size string>"\n'
            "    }\n"
            "  ]\n"
            "}\n"
            "```\n"
        )


def build_model():
    # TODO
    # return HailEvent
    return HailEvents
