"""
Represents articles and its fields
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict
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
    extracted_data: Optional[Dict] = None

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

    def format_fields(self, fields: Optional[list] = None) -> str:
        """
        Get a string representation of specified fields in the article.
        If no fields are specified, headline, date, and body are included.
        """
        if fields is None:
            fields = ["headline", "date", "body"]

        values = []
        headline = self.headline if "headline" in fields else ""
        date_str = ""
        if "date" in fields:
            date_str = self.date.strftime("%A, %B %d, %Y")
        body = self.body if "body" in fields else ""

        result = ""
        if headline:
            result += f"{headline}\n"
        if date_str:
            result += f"Published date: {date_str}\n\n"
        if body:
            result += f"{body}"
        return result.strip()
