import logging
import os

from app.schemas.tools import ToolResult, WorkspaceSearchInput

logger = logging.getLogger(__name__)

MAX_RESULTS = 20


def workspace_search(input: WorkspaceSearchInput) -> ToolResult:
    workspace_root = os.getenv("WORKSPACE_ROOT", ".")
    root = os.path.realpath(workspace_root)
    keyword = input.keyword.lower()
    matches = []

    try:
        for dirpath, _, filenames in os.walk(root):
            if any(skip in dirpath for skip in [".git", "__pycache__", "venv", ".venv", "node_modules"]):
                continue

            for filename in filenames:
                _, ext = os.path.splitext(filename)
                if ext not in input.file_extensions:
                    continue

                filepath = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(filepath, root)

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        for line_num, line in enumerate(f, 1):
                            if keyword in line.lower():
                                matches.append(f"{relative_path}:{line_num}: {line.strip()}")
                                if len(matches) >= MAX_RESULTS:
                                    break
                except (UnicodeDecodeError, PermissionError):
                    continue

                if len(matches) >= MAX_RESULTS:
                    break
            if len(matches) >= MAX_RESULTS:
                break

        if not matches:
            return ToolResult(success=True, result="No matches found.")

        logger.info(f"Search for '{input.keyword}': {len(matches)} matches")
        return ToolResult(success=True, result="\n".join(matches))

    except Exception as e:
        return ToolResult(success=False, error=f"Search failed: {e}")
