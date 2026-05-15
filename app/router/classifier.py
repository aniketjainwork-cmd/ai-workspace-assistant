import json
import logging

from app.llm import get_llm_response
from app.prompts.intent_classification import INTENT_CLASSIFICATION_SYSTEM_PROMPT
from app.schemas.intent import IntentClassification
from app.utils.parsing import strip_json_fences

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.6


def classify_intent(user_input: str) -> IntentClassification:
    raw_response = get_llm_response(
        system_prompt=INTENT_CLASSIFICATION_SYSTEM_PROMPT,
        user_prompt=user_input,
    )

    cleaned = strip_json_fences(raw_response)
    data = json.loads(cleaned)
    result = IntentClassification(**data)

    if result.confidence < CONFIDENCE_THRESHOLD:
        logger.info(f"Low confidence ({result.confidence}), overriding to 'irrelevant'")
        result = IntentClassification(
            intent="irrelevant",
            confidence=result.confidence,
            reasoning=result.reasoning,
        )

    logger.info(f"Classified intent: {result.intent} (confidence: {result.confidence})")
    return result
