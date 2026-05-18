import json
import logging
from typing import Type, TypeVar

from pydantic import BaseModel

from app.llm import get_llm_response
from app.utils.parsing import strip_json_fences

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def call_llm_with_validation(
    system_prompt: str,
    user_input: str,
    schema: Type[T],
    max_retries: int = 3,
) -> T:
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempt {attempt}/{max_retries}")

            raw_response = get_llm_response(
                system_prompt=system_prompt,
                user_prompt=user_input,
            )

            cleaned = strip_json_fences(raw_response)
            data = json.loads(cleaned)
            result = schema(**data)

            logger.info("Validation succeeded")
            return result

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                raise RuntimeError(
                    f"Failed to get valid structured output after {max_retries} attempts. "
                    f"Last error: {e}"
                ) from e

    raise RuntimeError("Unreachable")
