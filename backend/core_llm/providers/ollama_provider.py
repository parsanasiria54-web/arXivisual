import httpx
import time
import os
from typing import List
from ..interfaces import LLMProvider, LLMRequest, LLMResponse, ModelCapabilities, TokenUsage

class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    async def generate(self, request: LLMRequest) -> LLMResponse:
        start_time = time.time()

        # We'll use the Ollama Chat Completion API which is OpenAI compatible
        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": request.model,
            "messages": request.messages,
            "temperature": request.temperature,
        }
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        if request.response_format:
            payload["response_format"] = request.response_format

        if request.provider_kwargs:
            # We map options directly if using the native API, but since we are using /v1/chat/completions,
            # we might need to nest them under some Ollama specific fields depending on the exact version.
            # Usually /v1/chat/completions accepts standard fields and drops extras or maps them.
            # Native Ollama API takes 'options': {...}
            pass

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()

        end_time = time.time()
        latency = (end_time - start_time) * 1000

        content = data["choices"][0]["message"]["content"]

        usage = data.get("usage", {})
        token_usage = TokenUsage(
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0)
        )

        return LLMResponse(
            content=content,
            model_used=request.model,
            usage=token_usage,
            latency_ms=latency
        )

    async def health_check(self) -> bool:
        url = f"{self.base_url}/api/tags"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> List[ModelCapabilities]:
        url = f"{self.base_url}/api/tags"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
                response.raise_for_status()
                data = response.json()

            models = []
            for m in data.get("models", []):
                # Basic inference of capabilities
                supports_json = "7b" in m["name"].lower() or "8b" in m["name"].lower() or "20b" in m["name"].lower()
                models.append(ModelCapabilities(
                    name=m["name"],
                    provider="ollama",
                    context_window=8192, # Default assumption, could be queried specifically
                    supports_json=supports_json,
                    supports_streaming=True
                ))
            return models
        except Exception:
            return []
