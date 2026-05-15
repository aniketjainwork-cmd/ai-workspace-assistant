# AI Workspace Assistant

A CLI-based AI assistant that uses structured JSON outputs with Pydantic validation. Designed as a foundation for building RAG pipelines, tool-use agents, and LangGraph workflows.

## Architecture

```
ai_workspace_assistant/
├── app/
│   ├── llm/          # Reusable OpenAI-compatible client wrapper
│   ├── prompts/      # System prompt templates
│   ├── schemas/      # Pydantic models for structured outputs
│   ├── workflows/    # Orchestration logic (LLM call → parse → validate → retry)
│   └── utils/        # Parsing helpers (e.g., strip markdown fences)
├── main.py           # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

**Key design decisions:**
- **No frameworks** — raw OpenAI SDK + Pydantic only, keeping the code transparent and educational.
- **Provider-agnostic** — swap between Groq, OpenAI, or any OpenAI-compatible API by changing environment variables.
- **Structured outputs** — the LLM is prompted to return raw JSON; the response is parsed and validated against a Pydantic schema.
- **Retry logic** — if the LLM returns malformed JSON or validation fails, the workflow retries up to 3 times before raising.

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API key and provider settings
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_API_KEY` | API key for your LLM provider | `gsk_abc123...` |
| `LLM_BASE_URL` | Base URL for the OpenAI-compatible API | `https://api.groq.com/openai/v1` |
| `LLM_MODEL` | Model identifier | `llama-3.3-70b-versatile` |

## Usage

```bash
python main.py
```

Then paste a support ticket and press `Ctrl+D` (macOS/Linux) or `Ctrl+Z` (Windows) to submit.

### Example

**Input:**
```
I've been trying to reset my password for 3 days now and your system keeps
sending me expired links. This is incredibly frustrating. I have a demo with
a client tomorrow and I can't even access my account. Please fix this ASAP.
```

**Output:**
```
Analysis Result:
----------------------------------------
  Sentiment:    negative
  Priority:     high
  Summary:      Customer unable to reset password due to expired reset links, with urgent deadline.
  Action Items:
    - Investigate password reset link expiration logic
    - Manually reset the customer's password or provide alternative access
    - Escalate to engineering if link expiration is a systemic bug
```

## How Structured Outputs Work

1. **Prompt engineering** — the system prompt explicitly defines the JSON schema and instructs the LLM to return only raw JSON (no markdown fences, no explanation).
2. **Response cleaning** — `strip_json_fences()` removes any accidental markdown code fences the LLM might add.
3. **JSON parsing** — `json.loads()` converts the string to a Python dict.
4. **Pydantic validation** — the dict is passed to `TicketAnalysis(**data)`, which validates types and required fields.
5. **Retry loop** — if any step (2-4) fails, the entire LLM call is retried up to 3 times.

This pattern gives you type-safe, validated outputs from any LLM without relying on provider-specific "JSON mode" features.

## Next Steps

This project is designed to scale into:
- **RAG** — add vector search to inject relevant context into prompts
- **Tool use** — let the LLM call functions (file search, web lookup, database queries)
- **Agents** — multi-step reasoning with tool selection
- **LangGraph workflows** — stateful, graph-based orchestration with branching and cycles
