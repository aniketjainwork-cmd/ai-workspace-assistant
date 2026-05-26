from pydantic import BaseModel


class Task(BaseModel):
    description: str
    priority: str
    assignee: str


class ExtractedTasks(BaseModel):
    tasks: list[Task]
