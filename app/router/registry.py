import logging
from typing import Any, Callable, Dict

from app.schemas.intent import IntentType
from app.workflows import analyze_support_ticket

logger = logging.getLogger(__name__)

WORKFLOW_REGISTRY: Dict[IntentType, Callable[[str], Any]] = {
    IntentType.TICKET_ANALYSIS: analyze_support_ticket,
}


def route_to_workflow(intent: IntentType, user_input: str) -> Any:
    workflow = WORKFLOW_REGISTRY.get(intent)

    if workflow is None:
        logger.warning(f"No workflow registered for intent: {intent}")
        return None

    logger.info(f"Routing to workflow: {intent.value}")
    return workflow(user_input)
