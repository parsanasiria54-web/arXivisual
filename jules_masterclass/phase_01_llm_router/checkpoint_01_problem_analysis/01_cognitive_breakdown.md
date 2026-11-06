# Cognitive Breakdown: Decoupling LLM Execution

## The Problem
The current arXivisual architecture relies on statically configured, cloud-bound LLM API calls (primarily Azure OpenAI/GPT-5 family). While powerful, this tight coupling creates significant friction for several key use cases:
1. **Offline/Local Development:** Developers without active Azure subscriptions or internet access cannot run the agent pipeline locally.
2. **Hybrid Workloads:** Educational content generation often involves computationally expensive tasks (like reasoning out a Manim animation storyboard) that could be offloaded to free cloud tiers (Google Gemini, OpenRouter) or local high-capability open-weight models (gpt-oss:20b, qwen2.5:7b).
3. **Resilience & Fallback:** Statically bound API clients fail catastrophically if the specific provider goes down or rate-limits the user.

## First-Principles Decomposition
To solve this, we must decompose the concept of "LLM Execution" into distinct, isolated responsibilities:

1. **The Contract (Interfaces):**
   - Agents should not care *how* their prompt is executed, only that they send an `LLMRequest` (prompt, system instruction, schema) and receive an `LLMResponse` (content, token counts, latency).

2. **The Execution Engine (Providers):**
   - We need self-contained modules that know how to translate an `LLMRequest` into a specific provider's API format (Ollama, OpenAI-compatible).

3. **The Orchestrator (Router):**
   - A central service that receives the request, selects the appropriate provider based on user preference or dynamic health metrics, executes the request with resilience (retries, backoff), and standardizes the output.
   - Crucially, it must handle quirks of specific models (e.g., extracting clean JSON/code from reasoning models that use `<think>` tags).

## Conclusion
By abstracting the LLM execution layer, we enable a plug-and-play architecture where agents remain oblivious to the underlying engine, freeing the system to intelligently route workloads across local GPUs and diverse cloud providers.
