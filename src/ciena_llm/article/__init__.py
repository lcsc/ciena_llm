"""
Represents articles and its fields
"""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from datetime import datetime


@dataclass(order=True)
class Article:
    """
    Represents an article with its fields
    """

    filename: str
    date: datetime
    url: str
    headline: str
    body: str
    # TODO remove drought specific fields
    drought: Optional[bool] = None
    impacts: Optional[List] = None
    locations: Optional[List[str]] = None
    # TODO generalize to any type of event
    hail_event: Optional[dict] = None

    def to_dict(self):
        """
        Convert dataclass to dictionary
        """
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Convert dictionary to dataclass
        """
        return cls(**data)

    def get_headline_and_body(self, separator: str = "~") -> str:
        """
        Get string with headline and body with a custom separator
        """
        return f"{self.headline}{separator}{self.body}"

    def get_headline_and_body_and_date(self) -> str:
        """
        Get string with headline, body, and date
        """

        date = self.date
        formatted_date = date.strftime("%A, %B %d, %Y")

        return f"{self.headline}\nPublished date: {formatted_date}\n\n{self.body}"
