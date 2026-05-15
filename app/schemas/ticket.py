from pydantic import BaseModel


class TicketAnalysis(BaseModel):
    sentiment: str
    priority: str
    summary: str
    action_items: list[str]
