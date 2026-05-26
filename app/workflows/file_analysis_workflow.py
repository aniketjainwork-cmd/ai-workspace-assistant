import logging
from typing import Optional

from app.prompts.file_analysis import FILE_ANALYSIS_EXTRACTION_PROMPT
from app.schemas.file_analysis import FileAnalysisRequest
from app.schemas.tools import WorkflowContext, WorkflowStep
from app.tools import execute_tool
from app.utils.retry import call_llm_with_validation

logger = logging.getLogger(__name__)


def _step_from_result(tool_name: str, result) -> WorkflowStep:
    return WorkflowStep(
        tool=tool_name,
        success=result.success,
        result=result.result,
        data=result.data,
        error=result.error,
    )


def _try_read_or_find(filepath: str, context: WorkflowContext) -> Optional[str]:
    """Try direct read, fall back to file_find + read."""
    result = execute_tool("file_reader", {"filepath": filepath})
    context.steps.append(_step_from_result("file_reader", result))

    if result.success:
        return result.result

    logger.info(f"Direct read failed, searching for: {filepath}")
    find_result = execute_tool("file_find", {"filename": filepath})
    context.steps.append(_step_from_result("file_find", find_result))

    if not find_result.success:
        return None

    found_path = find_result.result
    read_result = execute_tool("file_reader", {"filepath": found_path})
    context.steps.append(_step_from_result("file_reader", read_result))

    if read_result.success:
        context.filepath = found_path
        return read_result.result

    return None


def analyze_file(user_input: str) -> WorkflowContext:
    """Read a file, summarize it, and extract tasks — with search fallback."""
    request = call_llm_with_validation(
        system_prompt=FILE_ANALYSIS_EXTRACTION_PROMPT,
        user_input=user_input,
        schema=FileAnalysisRequest,
    )

    context = WorkflowContext(filepath=request.filepath)

    file_content = _try_read_or_find(request.filepath, context)
    if file_content is None:
        logger.error("Could not read file — stopping workflow")
        return context

    # Summarize
    logger.info("Summarizing file content")
    result = execute_tool("note_summarizer", {"text": file_content})
    context.steps.append(_step_from_result("note_summarizer", result))

    if not result.success:
        logger.error(f"Summarization failed: {result.error}")
        return context

    # Extract tasks
    logger.info("Extracting tasks from file content")
    result = execute_tool("task_extractor", {"text": file_content})
    context.steps.append(_step_from_result("task_extractor", result))

    return context
