import os
import logging
from typing import Optional

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )
    return _client


def get_llm_response(system_prompt: str, user_prompt: str) -> str:
    client = _get_client()
    model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

    logger.info(f"Calling LLM model: {model}")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content
    logger.debug(f"Raw LLM response: {content}")
    return content
