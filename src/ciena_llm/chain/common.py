import logging
from typing import Dict, Any

import pydantic
from pydantic import BaseModel
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables.base import Runnable


def invoke_chain(
    chain: Runnable,
    input: str,
    response_class: BaseModel,
    error_response: Dict[str, Any],
    response_parsing: bool = True,
    **kwargs: Any,
) -> str | BaseModel:
    """
    Invokes a chain with the given input and processes the response.

    Args:
        chain (Runnable): The chain object that has an `invoke` method.
        input (str): The input text to be processed by the chain.
        response_class (Type[BaseModel]): The class to be used for parsing the response.
        error_response (Dict[str, Any]): The default response to be used in case of an error.
        response_parsing (bool, optional): Flag to determine if the response should be parsed. Defaults to True.
        **kwargs (Any): Additional keyword arguments to be passed to the chain's `invoke` method.

    Returns:
        str | BaseModel: The parsed response object or the raw output in case `response_parsing` is False.
    """
    try:
        # Invoke the chain
        output = chain.invoke({"text": input, **kwargs})

        if response_parsing:
            # Parse the response
            parsed_response = response_class(**output)

            return parsed_response

        # Return the raw output
        return output
    except pydantic.ValidationError as e:
        logging.error("pydantic.ValidationError: Failed to parse response: %s", e)
        print(f"OUTPUT: {output}")
        # TODO Handle this error
        # raise e

        # Return the default error response
        return response_class(**error_response)

    except OutputParserException as e:
        logging.error("OutputParserException: Failed to parse response: %s", e)
        # TODO Handle this error
        # raise e

        # Return the default error response
        return response_class(**error_response)
