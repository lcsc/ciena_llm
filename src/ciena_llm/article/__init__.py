"""
Represents articles and its fields
"""

from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass(order=True)
class Article:
    """
    Represents an article with its fields
    """

    filename: str
    date: str
    url: str
    headline: str
    body: str
    drought: Optional[bool] = None
    impacts: Optional[List] = None
    locations: Optional[List[str]] = None

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
