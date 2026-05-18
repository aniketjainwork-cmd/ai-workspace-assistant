from enum import Enum

from pydantic import BaseModel


class IntentType(str, Enum):
    TICKET_ANALYSIS = "ticket_analysis"
    IRRELEVANT = "irrelevant"


class IntentClassification(BaseModel):
    intent: IntentType
    confidence: float
    reasoning: str
