from pydantic import BaseModel


class NoteSummary(BaseModel):
    title: str
    summary: str
    key_points: list[str]
