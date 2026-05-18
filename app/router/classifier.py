import logging

from app.prompts.intent_classification import INTENT_CLASSIFICATION_SYSTEM_PROMPT
from app.schemas.intent import IntentClassification, IntentType
from app.utils.retry import call_llm_with_validation

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.6


def classify_intent(user_input: str) -> IntentClassification:
    result = call_llm_with_validation(
        system_prompt=INTENT_CLASSIFICATION_SYSTEM_PROMPT,
        user_input=user_input,
        schema=IntentClassification,
    )

    if result.confidence < CONFIDENCE_THRESHOLD:
        logger.info(f"Low confidence ({result.confidence}), overriding to 'irrelevant'")
        result = IntentClassification(
            intent=IntentType.IRRELEVANT,
            confidence=result.confidence,
            reasoning=result.reasoning,
        )

    logger.info(f"Classified intent: {result.intent} (confidence: {result.confidence})")
    return result
