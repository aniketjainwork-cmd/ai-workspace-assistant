import logging
from typing import Any, Dict

from pydantic import ValidationError

from app.tools.registry import TOOL_REGISTRY
from app.schemas.tools import ToolResult

logger = logging.getLogger(__name__)


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> ToolResult:
    if tool_name not in TOOL_REGISTRY:
        logger.error(f"Unknown tool: {tool_name}")
        return ToolResult(
            success=False,
            error=f"Unknown tool: {tool_name}. Available: {list(TOOL_REGISTRY.keys())}",
        )

    tool_def = TOOL_REGISTRY[tool_name]

    try:
        validated_input = tool_def.input_schema(**arguments)
    except ValidationError as e:
        logger.error(f"Invalid arguments for {tool_name}: {e}")
        return ToolResult(success=False, error=f"Invalid arguments: {e}")

    try:
        logger.info(f"Executing tool: {tool_name}")
        result = tool_def.function(validated_input)
        return result
    except Exception as e:
        logger.error(f"Tool execution failed ({tool_name}): {e}")
        return ToolResult(success=False, error=f"Tool execution failed: {e}")
