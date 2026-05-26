import json
import logging
import sys

from app.router import classify_intent, route_to_workflow
from app.schemas.intent import IntentType
from app.schemas.ticket import TicketAnalysis
from app.schemas.tools import WorkflowContext
from app.utils.synthesis import synthesize_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _format_workflow_for_synthesis(context: WorkflowContext) -> str:
    """Convert workflow context into a string for the synthesis LLM."""
    parts = []
    if context.filepath:
        parts.append(f"File: {context.filepath}")
    for step in context.steps:
        status = "SUCCESS" if step.success else "FAILED"
        parts.append(f"[{status}] {step.tool}")
        if step.data:
            parts.append(json.dumps(step.data, indent=2))
        elif step.result:
            parts.append(step.result)
        elif step.error:
            parts.append(f"Error: {step.error}")
    return "\n".join(parts)


def _format_ticket_for_synthesis(result: TicketAnalysis) -> str:
    """Convert ticket analysis into a string for the synthesis LLM."""
    items = "\n".join(f"  - {item}" for item in result.action_items)
    return (
        f"Sentiment: {result.sentiment}\n"
        f"Priority: {result.priority}\n"
        f"Summary: {result.summary}\n"
        f"Action Items:\n{items}"
    )


def main() -> None:
    print("AI Workspace Assistant")
    print("=" * 50)
    print("Paste your input below (press Ctrl+D or Ctrl+Z when done):\n")

    try:
        user_input = sys.stdin.read().strip()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)

    if not user_input:
        print("No input provided. Exiting.")
        sys.exit(1)

    print("\nClassifying intent...\n")

    try:
        intent_result = classify_intent(user_input)

        if intent_result.intent == IntentType.IRRELEVANT:
            print("This input doesn't match any supported workflow.")
            print(f"  Reason: {intent_result.reasoning}")
            print("\nSupported: ticket analysis, file analysis, file write, list workspace")
            sys.exit(0)

        print(f"Detected intent: {intent_result.intent.value} (confidence: {intent_result.confidence:.2f})")
        print("Running workflow...\n")

        result = route_to_workflow(intent_result.intent, user_input)

        if result is None:
            print("No workflow available for this intent.")
            sys.exit(1)

        # Format raw results for synthesis
        if isinstance(result, TicketAnalysis):
            raw_output = _format_ticket_for_synthesis(result)
        elif isinstance(result, WorkflowContext):
            raw_output = _format_workflow_for_synthesis(result)
        else:
            raw_output = str(result)

        # Synthesize natural language response
        print("-" * 40)
        response = synthesize_response(user_input, raw_output)
        print(response)
        print()

    except RuntimeError as e:
        logger.error(f"Workflow failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
