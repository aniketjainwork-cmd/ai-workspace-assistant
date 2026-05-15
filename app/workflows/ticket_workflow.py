import json
import logging

from app.llm import get_llm_response
from app.prompts import TICKET_ANALYSIS_SYSTEM_PROMPT
from app.schemas import TicketAnalysis
from app.utils.parsing import strip_json_fences

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def analyze_support_ticket(ticket_text: str) -> TicketAnalysis:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempt {attempt}/{MAX_RETRIES}")

            raw_response = get_llm_response(
                system_prompt=TICKET_ANALYSIS_SYSTEM_PROMPT,
                user_prompt=ticket_text,
            )

            cleaned = strip_json_fences(raw_response)
            data = json.loads(cleaned)
            result = TicketAnalysis(**data)

            logger.info("Validation succeeded")
            return result

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt == MAX_RETRIES:
                raise RuntimeError(
                    f"Failed to get valid structured output after {MAX_RETRIES} attempts. "
                    f"Last error: {e}"
                ) from e

    raise RuntimeError("Unreachable")
