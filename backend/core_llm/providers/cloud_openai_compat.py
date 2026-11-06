import httpx
import time
import os
from typing import List, Optional
from ..interfaces import LLMProvider, LLMRequest, LLMResponse, ModelCapabilities, TokenUsage

class CloudOpenAICompatProvider(LLMProvider):
    """Unified adapter for OpenAI-compatible endpoints (Gemini, OpenRouter, Groq, standard OpenAI)."""

    def __init__(self, base_url: str = None, api_key: str = None, provider_name: str = "openai-compat"):
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.provider_name = provider_name

        # Determine presets if base_url matches known services
        if "generativelanguage.googleapis.com" in self.base_url:
            self.provider_name = "gemini"
        elif "openrouter.ai" in self.base_url:
            self.provider_name = "openrouter"
        elif "api.groq.com" in self.base_url:
            self.provider_name = "groq"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        start_time = time.time()

        # Ensure we have chat completions endpoint
        url = self.base_url
        if not url.endswith("/chat/completions"):
            url = f"{url.rstrip('/')}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # OpenRouter specific headers
        if self.provider_name == "openrouter":
            headers["HTTP-Referer"] = "https://arxivisual.org"
            headers["X-Title"] = "arXivisual LLM Router"

        payload = {
            "model": request.model,
            "messages": request.messages,
            "temperature": request.temperature,
        }

        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        if request.response_format:
            payload["response_format"] = request.response_format

        # Add provider kwargs if any
        if request.provider_kwargs:
            payload.update(request.provider_kwargs)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=120.0)
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
        # Check standard models endpoint for health
        url = self.base_url
        if url.endswith("/chat/completions"):
            url = url.replace("/chat/completions", "/models")
        elif not url.endswith("/models"):
            url = f"{url.rstrip('/')}/models"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> List[ModelCapabilities]:
        # Implementation depends heavily on the provider, return some sensible defaults for known free models
        if self.provider_name == "gemini":
            return [
                ModelCapabilities(name="gemini-1.5-flash", provider="gemini", context_window=1000000, supports_json=True, supports_streaming=True),
                ModelCapabilities(name="gemini-1.5-pro", provider="gemini", context_window=2000000, supports_json=True, supports_streaming=True)
            ]
        elif self.provider_name == "openrouter":
            return [
                ModelCapabilities(name="google/gemini-flash-1.5-exp", provider="openrouter", context_window=1000000, supports_json=True, supports_streaming=True),
                ModelCapabilities(name="meta-llama/llama-3.1-8b-instruct:free", provider="openrouter", context_window=131072, supports_json=True, supports_streaming=True)
            ]
        elif self.provider_name == "groq":
            return [
                ModelCapabilities(name="llama3-8b-8192", provider="groq", context_window=8192, supports_json=True, supports_streaming=True),
                ModelCapabilities(name="mixtral-8x7b-32768", provider="groq", context_window=32768, supports_json=True, supports_streaming=True)
            ]
        return []
