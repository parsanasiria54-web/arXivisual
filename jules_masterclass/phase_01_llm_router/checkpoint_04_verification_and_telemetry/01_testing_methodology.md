# Testing Methodology: Deterministic Async LLM Routing

## The Problem
Testing LLM integration usually involves one of two bad options:
1. **Live APIs:** Requires paid API keys in CI, introduces flakiness due to network issues, and is slow.
2. **No Tests:** Code breaks in production when a provider changes their JSON structure.

## Our Approach: Mock Transports & Fault Injection

### 1. Mocking HTTP (httpx)
Instead of relying on live Ollama or Cloud endpoints, we use `unittest.mock.patch` to intercept calls to `httpx.AsyncClient.post` and `.get`. We return static JSON payloads that mimic the real responses from these providers. This ensures the parsing logic in `OllamaProvider` and `CloudOpenAICompatProvider` is tested deterministically.

### 2. Fault Injection for Resilience
A key feature of the `RouterService` is its exponential backoff. We test this by creating a mock provider where the `generate` method has a `side_effect` configured to raise an `Exception` (simulating a timeout) twice, and then return a valid `LLMResponse` on the third call. We patch `asyncio.sleep` to execute instantly so the test runs fast while still proving the retry loop works.

### 3. Parsing Edge Cases
We wrote pure unit tests (no mocks required) for `extract_clean_code_and_reasoning` to ensure regex handling of `<think>` tags and markdown code blocks (````json`) works flawlessly across various permutations.

See `02_execution_logs_and_report.md` for test output.
