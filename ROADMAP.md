# Roadmap

Future improvements to implement as the project grows.

## Deferred

### Base Workflow Interface
**Trigger:** Add when a second workflow shares setup logic, workflows need shared state, or LangGraph integration starts.

**Approach:** Use a `Protocol` (structural typing) rather than an ABC:
```python
class Workflow(Protocol):
    def run(self, user_input: str) -> BaseModel: ...
```

**Why not now:** Only one workflow exists as a plain function. The `Callable[[str], Any]` registry already provides a uniform interface. Abstraction without multiple consumers is just ceremony.

### Structured Logging with Context
**Trigger:** Add when running concurrent requests, shipping logs to an observability platform (Datadog, CloudWatch), or needing to trace a single request across multiple workflows.

**Approach:** Add correlation IDs and structured `extra` fields:
```python
logger.info("Classified intent", extra={
    "intent": "ticket_analysis",
    "confidence": 0.92,
    "request_id": "abc-123",
})
```

**Why not now:** Python's `logging.getLogger(__name__)` already provides module-level context (e.g., `app.router.classifier`). Current single-request, sequential execution makes this sufficient for debugging.

### Generic Workflow Execution Engine
**Trigger:** Add when workflows have multiple steps, need middleware (auth, rate limiting, caching), or require workflow-level observability (timing, token usage, step tracing).

**Approach:** A centralized executor:
```python
execute_workflow(
    workflow_name="ticket_analysis",
    schema=TicketAnalysis,
    prompt=TICKET_ANALYSIS_SYSTEM_PROMPT,
    input=user_input,
)
```

This becomes a mini orchestration runtime and a natural transition path into LangGraph when you need stateful, graph-based orchestration with branching and cycles.

**Why not now:** `call_llm_with_validation()` + the router registry already handles the current single-step pattern. No workflows yet require multi-step execution, middleware, or composition.

### Reusable Recovery Policies
**Trigger:** Add when multiple workflows share the same fallback patterns (retry with different params, graceful degradation, partial results).

**Approach:** Extract common recovery logic into composable policies:
```python
with recovery_policy(fallback=partial_result, max_retries=2):
    result = execute_tool(...)
```

**Why not now:** Workflows currently have simple, workflow-specific recovery (e.g., file_analysis falls back to file_find). No shared pattern has emerged yet.

### Presentation Layer Separation
**Trigger:** Add when output targets grow beyond CLI (API responses, web UI, Slack messages).

**Approach:** Split display logic from `main.py` into a `formatters/` layer with output-specific renderers:
```python
render(result, format="cli")  # or "json", "slack", "html"
```

**Why not now:** Only one output target (CLI). The display functions in `main.py` are adequate for a single consumer.

### ToolResult Status Enum
**Trigger:** Add when tools need to distinguish between retryable errors, fatal errors, and validation failures — especially when an orchestrator needs to decide whether to retry or abort.

**Approach:** Replace `success: bool` with a status enum:
```python
class ToolStatus(str, Enum):
    SUCCESS = "success"
    RETRYABLE_ERROR = "retryable_error"
    FATAL_ERROR = "fatal_error"
    VALIDATION_ERROR = "validation_error"
```

**Why not now:** Current tools have binary outcomes (worked or didn't). No orchestration logic yet needs to differentiate error types for decision-making.

### Workflow-Specific Typed Contexts
**Trigger:** Add when a workflow needs context fields that make no sense on other workflows (e.g., `FileAnalysisContext.search_attempts` vs `FileWriteContext.backup_path`).

**Approach:** Subclass or replace the generic `WorkflowContext`:
```python
class FileAnalysisContext(WorkflowContext):
    search_fallback_used: bool = False
    file_size_bytes: int = 0
```

**Why not now:** `WorkflowContext` with optional fields is generic enough for 3 workflows. The pain of one mega-context hasn't materialized yet.

### Task-Centric Intent Classification
**Trigger:** Add when implementing LLM-driven tool selection (agentic loops) where the LLM plans which tools to call based on user goals.

**Approach:** Shift from tool-oriented intents ("analyze this file") to goal-oriented intents ("what are today's blockers?"). The LLM would decompose a vague goal into a tool sequence:
```
"What are today's blockers?"
  → search recent files → extract tasks → filter by priority → synthesize
```

**Why not now:** This requires agentic reasoning — the LLM deciding which tools to call and in what order. Current architecture uses hardcoded workflow sequences, which is simpler and more predictable. Implement when adding LLM-driven orchestration loops.

### File Metadata Tool
**Trigger:** Add when building RAG, smart retrieval, or "summarize files modified today" workflows that need to filter files before reading them.

**Approach:** A `file_metadata` tool returning structured info:
```python
class FileMetadata(BaseModel):
    filepath: str
    size_bytes: int
    modified_at: datetime
    extension: str
```

**Why not now:** `list_files` already returns modification timestamps. Standalone metadata only matters when filtering large file collections before expensive LLM calls (i.e., RAG pre-filtering). Current workspace size doesn't warrant it.
