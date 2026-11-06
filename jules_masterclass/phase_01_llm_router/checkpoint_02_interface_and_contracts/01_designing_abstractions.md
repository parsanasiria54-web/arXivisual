# Designing Abstractions: Pydantic Contracts and ABCs

## Goal
To build a system that can flawlessly swap between local execution (Ollama) and cloud execution (Gemini, OpenRouter) without breaking downstream agent pipelines.

## The Approach: Strong Contracts
We achieve this through strict typing and Pydantic validation. The `backend/core_llm/interfaces.py` file is the heart of this decoupling.

### 1. `LLMRequest`: Normalizing Inputs
Different providers expect different payload structures. OpenAI takes `{"messages": [...]}`, while native Ollama historically took `{"prompt": "..."}`.
By enforcing an `LLMRequest` Pydantic model:
*   **Uniformity:** We force agents to speak a common language (standard chat messages).
*   **Extensibility:** We include `provider_kwargs` to allow passing highly specific parameters (like `num_ctx` for Ollama's context window) without polluting the global schema.

### 2. `LLMResponse`: Normalizing Outputs and Telemetry
The core value of an enterprise router is not just getting the text, but getting the metadata.
*   `latency_ms` and `usage` (`TokenUsage`): Essential for building a cost-tracking and performance-monitoring layer in later phases.
*   `reasoning_trace`: Open-source models (like DeepSeek-R1 or generalized coding models like `gpt-oss:20b`) often dump reasoning inside `<think>...</think>` blocks. We extract this so agents get clean JSON/code in `content`, but the system still records *why* the model made those choices in `reasoning_trace`.

### 3. `LLMProvider`: The Abstract Base Class
The Python `abc.ABC` enforces that any provider we build *must* implement `generate`, `health_check`, and `list_models`. If a developer forgets one, the application fails at instantiation, not at runtime during a user request.

## Snapshot
See `snapshot_interfaces.py` in this directory for the implemented code.
