import logging
import os

from app.schemas.tools import FileReaderInput, ToolResult

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".txt", ".md", ".py", ".json", ".yaml", ".yml", ".toml", ".cfg"}


def file_reader(input: FileReaderInput) -> ToolResult:
    workspace_root = os.getenv("WORKSPACE_ROOT", ".")
    filepath = os.path.join(workspace_root, input.filepath)

    filepath = os.path.realpath(filepath)
    root = os.path.realpath(workspace_root)
    if not filepath.startswith(root):
        return ToolResult(success=False, error="Access denied: path is outside workspace root")

    _, ext = os.path.splitext(filepath)
    if ext and ext not in ALLOWED_EXTENSIONS:
        return ToolResult(success=False, error=f"Unsupported file type: {ext}")

    if not os.path.exists(filepath):
        return ToolResult(success=False, error=f"File not found: {input.filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info(f"Read file: {input.filepath} ({len(content)} chars)")
        return ToolResult(success=True, result=content)
    except Exception as e:
        return ToolResult(success=False, error=f"Failed to read file: {e}")
