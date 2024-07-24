import json
import logging

from seqia.article import Article


def parse_response(article: Article, response: str) -> (Article, bool):

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
        {impact["impact_class"] for impact in result["impacts"]}
    )

    return (article, True)
