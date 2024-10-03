from typing import List, Optional

from pydantic import BaseModel, Field, root_validator


LOCATION_TYPES = [
    "country",
    # "region",
    "province",
    "state",
    "autonomous community",
    "county",
    "municipality",
    "city",
    "town",
    "village",
    "river",
    "basin",
    "dam",
    "lake",
    "mountain range",
    "other",
    "unknown",
]

LOCATION_NAME_DESCRIPTION = "Name of the location. Must be only the proper name of the location without any additional information."
LOCATION_TYPE_DESCRIPTION = f"Type of the location. Must be one of: {', '.join(LOCATION_TYPES)}. If the location is not one of the predefined types, select 'other' and provide a 'location_type_suggestion' for the type"


class LocationLLMResponse(BaseModel):
    location_name: str = Field(
        description=LOCATION_NAME_DESCRIPTION,
    )
    location_type: str = Field(
        default="unknown",
        description=LOCATION_TYPE_DESCRIPTION,
    )
    location_type_suggestion: Optional[str] = Field(
        default=None,
        description="Suggested type of location when 'other' is selected",
    )
    impact: str = Field(
        description="Impact on the location in the language of the prompt",
    )

    @root_validator(pre=True)
    @classmethod
    def check_location_type(cls, values):
        location_type = values.get("location_type")
        if not location_type:
            values["location_type"] = "unknown"
        elif location_type not in LOCATION_TYPES:
            values["location_type_suggestion"] = location_type
            values["location_type"] = "other"
        return values


class LocationListLLMResponse(BaseModel):
    locations: List[LocationLLMResponse] = Field(
        default_factory=list,
        description="A list of locations, each with a name and type",
    )

    # class Config:
    #     validate_assignment = True  # Enable detailed validation
