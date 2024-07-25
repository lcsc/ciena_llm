import json
import logging
from typing import Optional, Dict

from seqia.article import Article


def parse_response_json(
    article: Article, response: str, impact_tags: Dict[str, str]
) -> (Article, bool):

    logging.debug(f"Response: {response}")

    # Load the response as a JSON object
    try:
        result = json.loads(response)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}")

        return (article, False)

    result_str = json.dumps(
        result, ensure_ascii=False, indent=2, separators=(",", ": ")
    )

    logging.debug(f"Response (parsed): {result_str}")

    article.drought = result["drought"]
    article.impacts_aggregated = list(
        {impact_tags[impact["impact_class"]] for impact in result["impacts"]}
    )

    return (article, True)


def parse_response_bool(response: str) -> Optional[bool]:
    response = response.strip().lower()
    # Ensure the response is exactly "true" or "false"
    if response not in {"true", "false"}:
        logging.error(f"Unexpected response: {response}")
        return None
    return response == "true"
