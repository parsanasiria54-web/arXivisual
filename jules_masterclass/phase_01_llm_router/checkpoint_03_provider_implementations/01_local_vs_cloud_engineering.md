# Local vs Cloud Engineering: Bridging the Gap

## The Challenge
Executing code locally via Ollama vs hitting a Cloud API involves fundamentally different failure modes and nuances.

### 1. Local Inference (Ollama)
*   **VRAM and Cold Starts:** When you request a model like `gpt-oss:20b`, Ollama has to load it into VRAM. If it's a cold start, this can take 10-30 seconds. We must configure HTTP clients with extended timeouts (e.g., `timeout=120.0`) to avoid dropping the connection before generation even begins.
*   **Model Discovery:** We dynamically poll `/api/tags` to see what the user actually has installed. This is crucial for local environments where we can't guarantee a specific model exists.
*   **Reasoning Models:** Many powerful open-weights models dump reasoning tokens natively. We implemented `extract_clean_code_and_reasoning` in the `RouterService` to cleanly strip `<think>` tags so the frontend and downstream agents get pure JSON/Python.

### 2. Cloud APIs (Gemini, OpenRouter, Groq)
*   **Rate Limits and 429s:** Free tiers and commercial endpoints enforce rate limits. Our `RouterService` implements a robust `_execute_with_retry` loop using exponential backoff to handle transient HTTP 429 or 500 errors gracefully.
*   **Unified Interface (OpenAI Compat):** Instead of writing custom clients for every cloud provider, we leverage the fact that almost all modern providers offer an OpenAI-compatible `/v1/chat/completions` endpoint. By parameterizing the `base_url` and `api_key`, one class (`CloudOpenAICompatProvider`) handles them all.

## Implementation Notes
See `snapshot_router_core.py` for the code handling retries and reasoning extraction.
