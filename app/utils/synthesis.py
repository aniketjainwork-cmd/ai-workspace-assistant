import json
import logging

from app.llm import get_llm_response
from app.prompts.response_synthesis import RESPONSE_SYNTHESIS_PROMPT

logger = logging.getLogger(__name__)


def synthesize_response(user_input: str, workflow_result: str) -> str:
    """Take raw workflow output and generate a natural language response."""
    prompt = f"User's original request: {user_input}\n\nWorkflow results:\n{workflow_result}"

    try:
        response = get_llm_response(
            system_prompt=RESPONSE_SYNTHESIS_PROMPT,
            user_prompt=prompt,
        )
        return response.strip()
    except Exception as e:
        logger.warning(f"Synthesis failed, falling back to raw output: {e}")
        return workflow_result
