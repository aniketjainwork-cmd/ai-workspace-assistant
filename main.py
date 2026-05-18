import logging
import sys

from app.router import classify_intent, route_to_workflow
from app.schemas.intent import IntentType
from app.schemas.ticket import TicketAnalysis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def display_ticket_analysis(result: TicketAnalysis) -> None:
    print("Analysis Result:")
    print("-" * 40)
    print(f"  Sentiment:    {result.sentiment}")
    print(f"  Priority:     {result.priority}")
    print(f"  Summary:      {result.summary}")
    print(f"  Action Items:")
    for item in result.action_items:
        print(f"    - {item}")


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
            print(f"This input doesn't match any supported workflow.")
            print(f"  Reason: {intent_result.reasoning}")
            print(f"\nSupported workflows: ticket analysis")
            sys.exit(0)

        print(f"Detected intent: {intent_result.intent} (confidence: {intent_result.confidence:.2f})")
        print(f"Running workflow...\n")

        result = route_to_workflow(intent_result.intent, user_input)

        if result is None:
            print("No workflow available for this intent.")
            sys.exit(1)

        if isinstance(result, TicketAnalysis):
            display_ticket_analysis(result)

    except RuntimeError as e:
        logger.error(f"Workflow failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
