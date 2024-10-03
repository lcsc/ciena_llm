import logging
from typing import List

from seqia.article import Article

from ciena_llm.response.location import LocationListLLMResponse


# TODO use
class LocationResponseValidator:
    def __init__(self):
        pass

    def __call__(
        self, articles: List[Article], location_responses: List[LocationListLLMResponse]
    ):
        for article, location_response in zip(articles, location_responses):
            self.validate_locations(article, location_response)

    def validate_locations(
        self, article: Article, location_response: LocationListLLMResponse
    ):
        """
        Validate the location responses extracted from the article.

        :param article: The article from which the locations were extracted.
        :param location_response: The extracted location responses.
        """
        for location in location_response.locations:
            self.validate_location(article, location)

    def validate_location(self, article: Article, location: LocationListLLMResponse):
        """
        Validate a single location response extracted from the article.

        :param article: The article from which the location was extracted.
        :param location: The extracted location response.
        """
        name = location.location_name
        article_text = article.get_headline_and_body(separator=". ")

        if name not in article_text:
            logging.warning("Location '%s' not found in article text.", name)
            raise ValueError(f"Location '{name}' not found in article text.")
        logging.debug("Location '%s' found in article text.", name)
