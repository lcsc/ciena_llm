"""
Article loader from different sources and using different schemas.
"""

from json import JSONDecodeError
from typing import List, Optional
import csv
from datetime import datetime
import json
import os
import re

from tqdm import tqdm

from ciena_llm.article import Article


class ArticleLoader:
    """
    Article loader from different sources and using different schemas.
    """

    def __init__(self):
        self.problematic_articles = []

    def __call__(
        self,
        path: str = None,
        file_list: List[str] = None,
    ) -> List[Article]:
        """
        Loads articles from a file path, checking for file type and existence.
        Excludes problematic and similar articles by default, providing progress bars for each step.

        Args:
            path: The path to the file or directory containing articles.
            file_list: The list of JSON files.

        Returns:
            A list of successfully loaded, non-problematic, and unique articles.
        """

        articles = []

        if path:
            if os.path.isdir(path):
                # Handle directory (assuming each file is a separate JSON article)
                print(f"\nLoading articles from directory '{path}'")
                articles = self._load_articles_from_directory(path)
            elif os.path.isfile(path):
                # Handle single file
                if path.endswith(".json"):
                    article = self._load_article_from_json_file(path)
                    if article:
                        articles.append(article)
                else:
                    raise ValueError(f"Unsupported file format: {path}")
            else:
                raise FileNotFoundError(f"File or directory not found: {path}")
        elif file_list:
            print("\nLoading articles from file list")
            articles = self._load_articles_from_list(file_list)
        else:
            raise ValueError(
                "ArticleLoader call did not receive either a 'path' or 'file_list'"
            )

        print(
            f"Number of problematic articles excluded: {len(self.problematic_articles)}"
        )

        print(f"Number of remaining articles: {len(articles)}")

        return articles

    def _load_articles_from_directory(self, path: str) -> List[Article]:
        """
        Loads articles from a directory, assuming each article is a separate JSON file.

        Args:
            path: The path to the directory containing JSON files.

        Returns:
            A list of loaded Article objects.
        """

        articles = []
        for dirpath, _, files in os.walk(path):
            print(f"Loading {len(files)} files.")
            for file in tqdm(files, desc="Loading"):
                if file.endswith(".json"):
                    article_path = os.path.join(dirpath, file)
                    article = self._load_article_from_json_file(article_path)
                    if article:
                        articles.append(article)
        return articles

    def _load_articles_from_list(self, file_list: List[str]) -> List[Article]:
        """
        Loads articles from a list of file names, assuming each article is a separate JSON file.

        Args:
            file_list: The list of JSON files.

        Returns:
            A list of loaded Article objects.
        """

        articles = []
        print(f"Loading {len(file_list)} files.")
        for file in tqdm(file_list, desc="Loading"):
            if file.endswith(".json"):
                article_path = os.path.join(file)
                article = self._load_article_from_json_file(article_path)
                if article:
                    articles.append(article)
        return articles

    def _load_article_from_json_file(self, filepath: str) -> Optional[Article]:
        """
        Loads a single article from a JSON file, handling potential errors in the file and its fields.
        """

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                article_json = json.load(f)

        except (JSONDecodeError, FileNotFoundError) as e:
            self.problematic_articles.append((filepath, f"ERROR_LOADING: {e}"))
            return None

        problems = []

        # Check if the schema type of the JSON is NewsArticle
        article_type = article_json.get("@type", "")
        if "NewsArticle" not in article_type:
            problems.append("NO_NEWS_ARTICLE_SCHEMA")

        # Extract article's headline
        headline = article_json.get("headline", None)
        # Check if article has headline
        if not headline:
            problems.append("NO_HEADLINE")
        else:
            headline = self.clean_text(headline)
        # Check if article's headline is too short
        if headline is not None and len(headline) == 0:
            problems.append(f"SHORT_HEADLINE({len(headline)})")

        # Extract article's body
        body = article_json.get("articleBody", None)
        # Check if article has body
        if not body:
            problems.append("NO_BODY")
        else:
            body = self.clean_text(body)
        # Check if article's body is too short or too long
        if body is not None and len(body) == 0:
            problems.append(f"SHORT_BODY({len(body)})")

        # Extract article's date
        date = article_json.get("datePublished", None)
        # Check if article has date
        if not date:
            problems.append("NO_DATE")
        else:
            try:
                date = date.split("T")[0]
                date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                problems.append(f"INVALID_DATE({date})")

        # Extract article's URL
        url = (
            article_json.get("mainEntityOfPage", {}).get("@id")
            if isinstance(article_json.get("mainEntityOfPage"), dict)
            else article_json.get("url")
        )
        # Check if article has URL
        if not url:
            problems.append("NO_URL")
        else:
            url = self.clean_text(url)

        if problems:
            self.problematic_articles.append((filepath, ",".join(problems)))
            return None

        return Article(
            filename=filepath,
            date=date,
            url=url,
            headline=headline,
            body=body,
        )

    def write_excluded_problematic_articles_to_csv(self, file):
        """
        Write the excluded problematic articles to a CSV file.
        """
        with open(file, "w", encoding="utf-8") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["filename", "reason"])
            for row in self.problematic_articles:
                csv_writer.writerow(row)

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
