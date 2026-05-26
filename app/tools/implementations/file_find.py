import logging
import os

from app.schemas.tools import FileFindInput, ToolResult

logger = logging.getLogger(__name__)


def file_find(input: FileFindInput) -> ToolResult:
    workspace_root = os.getenv("WORKSPACE_ROOT", ".")
    root = os.path.realpath(workspace_root)
    target = input.filename.lower()

    for dirpath, _, filenames in os.walk(root):
        if any(skip in dirpath for skip in [".git", "__pycache__", "venv", ".venv", "node_modules"]):
            continue
        for f in filenames:
            if f.lower() == target or target in f.lower():
                found_path = os.path.relpath(os.path.join(dirpath, f), root)
                logger.info(f"Found file: {found_path}")
                return ToolResult(success=True, result=found_path)

    return ToolResult(success=False, error=f"No file matching '{input.filename}' found in workspace")
