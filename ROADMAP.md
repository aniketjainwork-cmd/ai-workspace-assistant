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
