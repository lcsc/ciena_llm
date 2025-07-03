from typing import List, Optional
from pydantic import BaseModel, Field


class HailEvent(BaseModel):
    locations: List[str] = Field(
        default_factory=list,
        description="List of locations directly affected by the hail event.",
    )
    date: Optional[str] = Field(
        default=None,
        description="Date of the hail event (format: YYYY-MM-DD HH:mm or YYYY-MM-DD).",
    )
    date_text: Optional[str] = Field(
        default=None,
        description="Textual representation of the date of the hail event, if the date cannot be inferred from the text.",
    )
    duration: Optional[str | int] = Field(
        default=None,
        description="Duration of the hail event in minutes",
    )
    duration_text: Optional[str] = Field(
        default=None,
        description="Textual representation of the duration of the hail event, if the duration cannot be inferred from the text.",
    )
    damages: List[str] = Field(
        default_factory=list,
        description="List of damages caused by the hail event.",
    )
    size: Optional[str] = Field(
        default=None,
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
