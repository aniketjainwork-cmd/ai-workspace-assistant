from enum import Enum

from pydantic import BaseModel


class IntentType(str, Enum):
    TICKET_ANALYSIS = "ticket_analysis"
    FILE_ANALYSIS = "file_analysis"
    FILE_WRITE = "file_write"
    LIST_WORKSPACE = "list_workspace"
    IRRELEVANT = "irrelevant"


class IntentClassification(BaseModel):
    intent: IntentType
    confidence: float
    reasoning: str
