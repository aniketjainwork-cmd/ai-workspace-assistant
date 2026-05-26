from typing import Any, List, Optional

from pydantic import BaseModel


# --- Tool execution result ---

class ToolResult(BaseModel):
    success: bool
    result: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None


# --- Workflow orchestration types ---

class WorkflowStep(BaseModel):
    tool: str
    success: bool
    result: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None


class WorkflowContext(BaseModel):
    filepath: Optional[str] = None
    overwrite: Optional[bool] = None
    append: Optional[bool] = None
    steps: List[WorkflowStep] = []


# --- Tool input schemas ---

class FileReaderInput(BaseModel):
    filepath: str


class FileWriterInput(BaseModel):
    filepath: str
    content: str
    overwrite: bool = False
    append: bool = False


class FileFindInput(BaseModel):
    filename: str


class ListFilesInput(BaseModel):
    file_extensions: list = [".txt", ".md", ".py", ".json", ".yaml", ".yml"]
    limit: int = 20


class NoteSummarizerInput(BaseModel):
    text: str


class TaskExtractorInput(BaseModel):
    text: str


class WorkspaceSearchInput(BaseModel):
    keyword: str
    file_extensions: list = [".txt", ".md", ".py"]
