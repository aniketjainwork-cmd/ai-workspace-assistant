import logging

from app.prompts.note_summarizer import SUMMARIZER_PROMPT
from app.schemas.summaries import NoteSummary
from app.schemas.tools import NoteSummarizerInput, ToolResult
from app.utils.retry import call_llm_with_validation

logger = logging.getLogger(__name__)


def note_summarizer(input: NoteSummarizerInput) -> ToolResult:
    try:
        result = call_llm_with_validation(
            system_prompt=SUMMARIZER_PROMPT,
            user_input=input.text,
            schema=NoteSummary,
        )
        logger.info(f"Summarized note: {result.title}")
        return ToolResult(success=True, data=result.model_dump())
    except RuntimeError as e:
        return ToolResult(success=False, error=str(e))
