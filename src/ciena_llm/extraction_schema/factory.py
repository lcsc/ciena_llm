from typing import Dict, Type, Optional

from pydantic import BaseModel

from ciena_llm.extraction_schema.impact import build_model as build_impact_model
from ciena_llm.extraction_schema.province import build_model as build_province_model
from ciena_llm.extraction_schema.event import build_model as build_event_model


class ExtractionSchemaFactory:
    """
    Factory class to create dynamic extraction schema models
    """

    @classmethod
    def get_extraction_schema(
        cls,
        stage: str,
        config: Dict,
    ) -> Type[BaseModel]:
        """
        Factory function to create a dynamic extraction schema model.

        :param stage: The extraction stage
        :param language: The language of the extraction schema
        :param config: The configuration
        :return: A dynamically created Pydantic model
        """

        event = config.get("event").get("tag")

        if stage == "event_identification":
            return build_event_model(event)

        if stage == "impact_extraction":
            impacts = [impact.get("tag") for impact in config.get("impacts")]
            return build_impact_model(event, impacts)

        if stage == "location_extraction":
            return build_province_model(event)

        raise ValueError(f"Stage {stage} not supported")
