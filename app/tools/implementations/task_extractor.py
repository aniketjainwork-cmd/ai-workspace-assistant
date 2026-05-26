import logging

from app.prompts.task_extractor import TASK_EXTRACTOR_PROMPT
from app.schemas.tasks import ExtractedTasks
from app.schemas.tools import TaskExtractorInput, ToolResult
from app.utils.retry import call_llm_with_validation

logger = logging.getLogger(__name__)


def task_extractor(input: TaskExtractorInput) -> ToolResult:
    try:
        result = call_llm_with_validation(
            system_prompt=TASK_EXTRACTOR_PROMPT,
            user_input=input.text,
            schema=ExtractedTasks,
        )
        logger.info(f"Extracted {len(result.tasks)} tasks")
        return ToolResult(success=True, data=result.model_dump())
    except RuntimeError as e:
        return ToolResult(success=False, error=str(e))
