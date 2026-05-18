from app.prompts import TICKET_ANALYSIS_SYSTEM_PROMPT
from app.schemas import TicketAnalysis
from app.utils.retry import call_llm_with_validation


def analyze_support_ticket(ticket_text: str) -> TicketAnalysis:
    return call_llm_with_validation(
        system_prompt=TICKET_ANALYSIS_SYSTEM_PROMPT,
        user_input=ticket_text,
        schema=TicketAnalysis,
    )
