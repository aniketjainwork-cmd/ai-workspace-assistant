import logging
import os

from app.schemas.tools import FileWriterInput, ToolResult

logger = logging.getLogger(__name__)


def file_writer(input: FileWriterInput) -> ToolResult:
    workspace_root = os.getenv("WORKSPACE_ROOT", ".")
    filepath = os.path.join(workspace_root, input.filepath)

    filepath = os.path.realpath(filepath)
    root = os.path.realpath(workspace_root)
    if not filepath.startswith(root):
        return ToolResult(success=False, error="Access denied: path is outside workspace root")

    if os.path.exists(filepath) and not input.overwrite and not input.append:
        return ToolResult(
            success=False,
            error=f"File already exists: {input.filepath}. Set overwrite=True to replace or append=True to add content.",
        )

    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        mode = "a" if input.append else "w"
        with open(filepath, mode, encoding="utf-8") as f:
            if input.append:
                f.write("\n" + input.content)
            else:
                f.write(input.content)
        action = "appended to" if input.append else "written"
        logger.info(f"File {action}: {input.filepath} ({len(input.content)} chars)")
        return ToolResult(success=True, result=f"File {action}: {input.filepath}")
    except Exception as e:
        return ToolResult(success=False, error=f"Failed to write file: {e}")
