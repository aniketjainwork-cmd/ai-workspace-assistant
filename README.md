# AI Workspace Assistant

A CLI-based AI workspace assistant with intent routing, tool orchestration, and structured outputs. Built from fundamentals (no frameworks) as a foundation for RAG, agents, and LangGraph workflows.

## Architecture

```
ai_workspace_assistant/
├── app/
│   ├── llm/                    # Reusable OpenAI-compatible client wrapper
│   ├── prompts/                # All system prompt templates (centralized)
│   ├── router/                 # Intent classification + workflow routing
│   ├── schemas/                # All Pydantic models (centralized)
│   ├── tools/
│   │   ├── implementations/    # Tool functions (file_reader, file_writer, etc.)
│   │   ├── executor.py         # execute_tool() — validates, executes, returns ToolResult
│   │   └── registry.py         # TOOL_REGISTRY — maps tool names to ToolDefinitions
│   ├── utils/                  # Retry logic, parsing, response synthesis
│   └── workflows/              # Orchestration (chains tools into sequences)
├── main.py                     # CLI entry point
├── ROADMAP.md                  # Deferred architectural decisions
├── requirements.txt
└── .env.example
```

**Key design decisions:**
- **No frameworks** — raw OpenAI SDK + Pydantic only, keeping the code transparent and educational.
- **Provider-agnostic** — swap between Groq, OpenAI, or any OpenAI-compatible API via environment variables.
- **Intent routing** — LLM classifies user input into typed intents (enum), router dispatches to the correct workflow.
- **Tool orchestration** — workflows chain tools in hardcoded sequences via a centralized executor with typed inputs/outputs.
- **Structured outputs** — LLMs return raw JSON, validated by Pydantic schemas with retry logic.
- **Response synthesis** — raw workflow results are passed through a final LLM call for natural language output.

## Flow

```
User Input → Intent Classifier → Router → Workflow → Tools (via executor) → Synthesis → Response
```

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
| `WORKSPACE_ROOT` | Root directory for file tools | `.` |

## Supported Workflows

| Intent | Trigger examples | What it does |
|--------|-----------------|--------------|
| `ticket_analysis` | Support tickets, complaints, bug reports | Extracts sentiment, priority, summary, action items |
| `file_analysis` | "analyze README.md", "summarize the roadmap" | Reads file (with search fallback), summarizes, extracts tasks |
| `file_write` | "create notes/ideas.md with...", "add X to file.md" | Writes/appends content to files |
| `list_workspace` | "show my files", "what's in my workspace" | Lists recent workspace files with timestamps |

## Tools

| Tool | Type | Description |
|------|------|-------------|
| `file_reader` | System | Read files safely (path traversal protection, extension allowlist) |
| `file_writer` | System | Write/append files (overwrite protection, auto-mkdir) |
| `file_find` | System | Find files by name across workspace |
| `list_files` | System | List recent workspace files with timestamps |
| `workspace_search` | System | Keyword search across file contents |
| `note_summarizer` | LLM-powered | Summarize documents into title + key points |
| `task_extractor` | LLM-powered | Extract action items with priority + assignee |

## Usage

```bash
python main.py
```

Paste your input and press `Ctrl+D` (macOS/Linux) or `Ctrl+Z` (Windows).

### Examples

```bash
# Analyze a file
echo "summarize the roadmap" | python main.py

# Write a file
echo "create notes/todo.md with: finish the API integration" | python main.py

# Append to a file
echo "add 'write tests' to notes/todo.md" | python main.py

# List workspace files
echo "show me my files" | python main.py

# Support ticket analysis
echo "Payment gateway returning 500 errors for 2 hours. Customers can't checkout." | python main.py

# Irrelevant input (rejected)
echo "hey whats up" | python main.py
```

## How It Works

1. **Intent classification** — LLM classifies input into a typed `IntentType` enum with confidence scoring. Low confidence defaults to "irrelevant".
2. **Routing** — `WORKFLOW_REGISTRY` maps intent → workflow function.
3. **Workflow execution** — Workflow chains tools via `execute_tool()`, building a typed `WorkflowContext` with `WorkflowStep` results.
4. **Tool execution** — `execute_tool()` validates input against Pydantic schemas, runs the tool function, returns `ToolResult`.
5. **Response synthesis** — Final LLM call converts raw workflow output into a natural language response.

## Adding a New Tool

1. Create `app/tools/implementations/my_tool.py`
2. Add input schema to `app/schemas/tools.py`
3. Export from `app/tools/implementations/__init__.py`
4. Register in `app/tools/registry.py`

## Adding a New Workflow

1. Add intent to `IntentType` enum in `app/schemas/intent.py`
2. Add intent description to `app/prompts/intent_classification.py`
3. Create workflow in `app/workflows/`
4. Register in `app/router/registry.py`

## Next Steps

See [ROADMAP.md](ROADMAP.md) for deferred architectural decisions. This project is designed to evolve into:
- **RAG** — vector search to inject relevant context into prompts
- **Agentic tool selection** — LLM decides which tools to call (replaces hardcoded sequences)
- **LangGraph workflows** — stateful, graph-based orchestration with branching and cycles
