from typing import List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator


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
LOCATION_TYPE_DESCRIPTION = f"Type of the location. Must be one of: {', '.join(LOCATION_TYPES)}. Select a single type for each location."


class LocationLLMResponse(BaseModel):
    location_name: str = Field(
        description=LOCATION_NAME_DESCRIPTION,
    )
    location_type: str = Field(
        description=LOCATION_TYPE_DESCRIPTION,
    )
    location_type_suggestion: Optional[str] = Field(
        default=None,
        description="Suggested type of location when 'other' is selected",
    )
    location_provinces: List[str] = Field(
        description="List of provinces where the impacted location is",
    )

    @root_validator(pre=True)
    def check_location_type(cls, values):
        if values.get("location_type"):
            values["location_type"] = values["location_type"].lower()
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
