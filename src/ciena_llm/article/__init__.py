"""
Represents articles and its fields
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict
from datetime import datetime
from typing import List
import re

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

class BaseArticleLoader:
    """
    Abstract Class for Article Loaders.
    """
    def __init__(self):
        pass

    def __call__(
        self,
        path: str = None,
        file_list: List[str] = None,
    ) -> List[Article]:
        pass
    
    def write_excluded_problematic_articles_to_csv(self, file):
        """
        Write the excluded problematic articles to a CSV file.
        """
        pass

    def clean_text(self, text: str) -> str:
        """
        Remove extra characters from text.
        """

        # Cleans up some garbage HTML tags from news body text
        text = text.replace("&quot;", "'")
        text = text.replace("\xa0", " ")

        # Get all different quote styles and unify them under a unique one
        text = text.replace("“", '"')
        text = text.replace("”", '"')
        text = text.replace("«", '"')
        text = text.replace("»", '"')
        text = text.replace("'", '"')

        # Match and remove HTML tags like this one: &#039;
        text = re.sub(r"&#[0-9]+;", "", text)

        # Clean multiple spaces and output them as just one
        text = re.sub(r"\s\s+", " ", text)

        return text