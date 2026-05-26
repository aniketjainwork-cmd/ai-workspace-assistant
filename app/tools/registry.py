from typing import Any, Callable, Dict, Type

from pydantic import BaseModel

from app.tools.implementations import (
    file_find,
    file_reader,
    file_writer,
    list_files,
    note_summarizer,
    task_extractor,
    workspace_search,
)
from app.schemas.tools import (
    FileFindInput,
    FileReaderInput,
    FileWriterInput,
    ListFilesInput,
    NoteSummarizerInput,
    TaskExtractorInput,
    WorkspaceSearchInput,
)


class ToolDefinition(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    function: Callable
    input_schema: Type[BaseModel]
    description: str


TOOL_REGISTRY: Dict[str, ToolDefinition] = {
    "file_find": ToolDefinition(
        function=file_find,
        input_schema=FileFindInput,
        description="Find a file by name in the workspace",
    ),
    "file_reader": ToolDefinition(
        function=file_reader,
        input_schema=FileReaderInput,
        description="Read a file from the workspace",
    ),
    "file_writer": ToolDefinition(
        function=file_writer,
        input_schema=FileWriterInput,
        description="Write content to a file in the workspace",
    ),
    "note_summarizer": ToolDefinition(
        function=note_summarizer,
        input_schema=NoteSummarizerInput,
        description="Summarize a document or note using LLM",
    ),
    "task_extractor": ToolDefinition(
        function=task_extractor,
        input_schema=TaskExtractorInput,
        description="Extract actionable tasks from text using LLM",
    ),
    "list_files": ToolDefinition(
        function=list_files,
        input_schema=ListFilesInput,
        description="List recent files in the workspace",
    ),
    "workspace_search": ToolDefinition(
        function=workspace_search,
        input_schema=WorkspaceSearchInput,
        description="Search for keywords across workspace files",
    ),
}
