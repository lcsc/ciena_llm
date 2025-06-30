from typing import Dict, Type

from pydantic import BaseModel

from ciena_llm.extraction_schema.impact import build_model as build_impact_model
from ciena_llm.extraction_schema.province import build_model as build_province_model
from ciena_llm.extraction_schema.event import build_model as build_event_model
from ciena_llm.extraction_schema.hail_event import build_model as build_hail_model


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


        if stage == "event_identification":
            event = config.get("event").get("tag")
            return build_event_model(event)

        if stage == "impact_extraction":
            event = config.get("event").get("tag")
            impacts = [impact.get("tag") for impact in config.get("impacts")]
            return build_impact_model(event, impacts)

        if stage == "location_extraction":
            event = config.get("event").get("tag")
            return build_province_model(event)

        if stage == "hail_extraction":
            return build_hail_model()

        raise ValueError(f"Stage {stage} not supported")
