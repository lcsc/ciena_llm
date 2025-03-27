"""
Utility functions for writing data to files.
"""

from collections import OrderedDict
from typing import List, Callable
import csv
import json

from ciena_llm.article import Article


def write_articles_to_json(articles: List[Article], file: str):
    """
    Write a list of Article objects to a JSON file.

    Args:
        articles (List[Article]): List of Article objects.
        file (str): Path to the JSON file.

    Returns:
        None
    """
    articles = [article.to_dict() for article in articles]
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(articles))


def write_csv(file: str, data: List[dict]):
    """
    Write a list of dictionaries to a CSV file.

    Args:
        file (str): Path to the CSV file.
        data (List[dict]): List of dictionaries with data.

    Returns:
        None
    """
    if not data:
        print(f"Error: No data to write to {file}.")
        return
    with open(file, "w", encoding="utf-8") as f:
        keys = list(data[0].keys())
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def order_data(data: List[dict], keys: List[str]) -> List[dict]:
    """
    Order a list of dictionaries based on specified keys.

    Args:
        data (List[dict]): List of dictionaries to order.
        keys (List[str]): List of keys defining the order.

    Returns:
        List[dict]: Ordered list of dictionaries.
    """
    ordered_data = []
    for d in data:
        ordered_d = OrderedDict()
        for key in keys:
            if key in d:
                ordered_d[key] = d[key]
        ordered_data.append(ordered_d)
    return ordered_data


def extract_data_by_keys(data_obj, prefix: str, keys_to_include: List[str]) -> dict:
    """
    Extract data from an object and filter by keys.

    Args:
        data_obj: Object to extract data from.
        prefix (str): Prefix for keys.
        keys_to_include (List[str]): List of keys to include.

    Returns:
        dict: Filtered and prefixed dictionary.
    """
    return {
        f"{prefix}_{key}": getattr(data_obj, key)
        for key in data_obj.__dict__
        if f"{prefix}_{key}" in keys_to_include
    }


def extract_articles(articles: List[Article], keys_to_include: List[str]) -> List[dict]:
    """
    Extract specified attributes from Article objects.

    Args:
        articles (List[Article]): List of Article objects.
        keys_to_include (List[str]): List of keys to include.

    Returns:
        List[dict]: List of dictionaries with specified attributes.
    """
    return [
        extract_data_by_keys(article, "article", keys_to_include)
        for article in articles
    ]


def get_extraction_function(
    level: str,
) -> Callable[[List[Article], List[str]], List[dict]]:
    """
    Get the extraction function based on the level parameter.

    Args:
        level (str): The level of extraction ("article").

    Returns:
        Callable: The appropriate extraction function.
    """
    if level == "article":
        return extract_articles
    else:
        raise ValueError(f"Invalid level: {level}. Valid options are 'article'.")


def write_to_csv(
    articles: List[Article], file: str, keys_to_include: List[str], level: str
):
    """
    General function to write specific article data to a CSV file based on level.

    Args:
        articles (List[Article]): List of Article objects.
        file (str): Path to the CSV file.
        keys_to_include (List[str]): List of keys to include.
        level (str): The level of extraction ("article").

    Returns:
        None
    """
    extract_function = get_extraction_function(level)
    data = extract_function(articles, keys_to_include)
    if data:
        write_csv(file, data)
    else:
        print(f"No data to write to {file}.")
