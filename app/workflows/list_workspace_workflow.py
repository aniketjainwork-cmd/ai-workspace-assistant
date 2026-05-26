import logging

from app.schemas.tools import WorkflowContext, WorkflowStep
from app.tools import execute_tool

logger = logging.getLogger(__name__)


def list_workspace(user_input: str) -> WorkflowContext:
    """List recent files in the workspace."""
    context = WorkflowContext()

    result = execute_tool("list_files", {})
    context.steps.append(WorkflowStep(
        tool="list_files",
        success=result.success,
        result=result.result,
        error=result.error,
    ))

    return context
