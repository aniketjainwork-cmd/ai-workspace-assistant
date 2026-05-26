import logging
import os
from datetime import datetime

from app.schemas.tools import ListFilesInput, ToolResult

logger = logging.getLogger(__name__)

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules", ".claude"}


def list_files(input: ListFilesInput) -> ToolResult:
    workspace_root = os.getenv("WORKSPACE_ROOT", ".")
    root = os.path.realpath(workspace_root)
    files = []

    try:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

            for filename in filenames:
                _, ext = os.path.splitext(filename)
                if input.file_extensions and ext not in input.file_extensions:
                    continue

                filepath = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(filepath, root)
                mod_time = os.path.getmtime(filepath)
                files.append((relative_path, mod_time))

        files.sort(key=lambda x: x[1], reverse=True)
        files = files[:input.limit]

        if not files:
            return ToolResult(success=True, result="No files found in workspace.")

        lines = []
        for path, mtime in files:
            timestamp = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            lines.append(f"{timestamp}  {path}")

        logger.info(f"Listed {len(files)} workspace files")
        return ToolResult(success=True, result="\n".join(lines))

    except Exception as e:
        return ToolResult(success=False, error=f"Failed to list files: {e}")
