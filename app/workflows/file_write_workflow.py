import logging

from app.prompts.file_write import FILE_WRITE_EXTRACTION_PROMPT
from app.schemas.file_write import FileWriteRequest
from app.schemas.tools import WorkflowContext, WorkflowStep
from app.tools import execute_tool
from app.utils.retry import call_llm_with_validation

logger = logging.getLogger(__name__)


def write_file(user_input: str) -> WorkflowContext:
    """Extract write parameters from user input and write to a file."""
    request = call_llm_with_validation(
        system_prompt=FILE_WRITE_EXTRACTION_PROMPT,
        user_input=user_input,
        schema=FileWriteRequest,
    )

    context = WorkflowContext(
        filepath=request.filepath,
        overwrite=request.overwrite,
        append=request.append,
    )

    logger.info(f"Writing to: {request.filepath} (overwrite={request.overwrite}, append={request.append})")
    result = execute_tool("file_writer", {
        "filepath": request.filepath,
        "content": request.content,
        "overwrite": request.overwrite,
        "append": request.append,
    })

    context.steps.append(WorkflowStep(
        tool="file_writer",
        success=result.success,
        result=result.result,
        error=result.error,
    ))

    return context
