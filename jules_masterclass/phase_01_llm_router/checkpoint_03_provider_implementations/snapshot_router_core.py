import asyncio
import logging
import re
from typing import Dict, Optional, Tuple, Any
from .interfaces import LLMProvider, LLMRequest, LLMResponse
from .providers.ollama_provider import OllamaProvider
from .providers.cloud_openai_compat import CloudOpenAICompatProvider

logger = logging.getLogger(__name__)

class RouterService:
    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {
            "ollama": OllamaProvider(),
            "gemini": CloudOpenAICompatProvider(base_url="https://generativelanguage.googleapis.com/v1beta/openai/"),
            "openrouter": CloudOpenAICompatProvider(base_url="https://openrouter.ai/api/v1"),
            "groq": CloudOpenAICompatProvider(base_url="https://api.groq.com/openai/v1")
        }

    def extract_clean_code_and_reasoning(self, raw_text: str) -> Tuple[str, Optional[str]]:
        """
        Parses reasoning models' output.
        Extracts anything inside <think>...</think> into reasoning_trace.
        Returns the rest (clean text/json) and the reasoning_trace.
        """
        think_pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
        match = think_pattern.search(raw_text)

        reasoning_trace = None
        clean_text = raw_text

        if match:
            reasoning_trace = match.group(1).strip()
            # Remove the think block from the text
            clean_text = think_pattern.sub('', raw_text).strip()

        # Optional: remove markdown code blocks if we expect pure JSON
        # This is basic and might need refinement based on exact agent needs.
        if clean_text.startswith("```json"):
            clean_text = re.sub(r'^```json\s*', '', clean_text)
            clean_text = re.sub(r'\s*```$', '', clean_text)
        elif clean_text.startswith("```python"):
            clean_text = re.sub(r'^```python\s*', '', clean_text)
            clean_text = re.sub(r'\s*```$', '', clean_text)
        elif clean_text.startswith("```"):
            clean_text = re.sub(r'^```\w*\s*', '', clean_text)
            clean_text = re.sub(r'\s*```$', '', clean_text)

        return clean_text, reasoning_trace

    async def _execute_with_retry(self, provider: LLMProvider, request: LLMRequest, max_retries: int = 3) -> LLMResponse:
        """Executes the request with exponential backoff."""
        base_delay = 1.0

        for attempt in range(max_retries):
            try:
                return await provider.generate(request)
            except Exception as e:
                logger.warning(f"Provider generation failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
                # Exponential backoff
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
        raise RuntimeError("Unexpected end of retry loop")

    async def route_request(self, provider_name: str, request: LLMRequest) -> LLMResponse:
        """
        Routes the request to the specified provider and applies parsing/healing.
        """
        if provider_name not in self.providers:
            raise ValueError(f"Unknown provider: {provider_name}")

        provider = self.providers[provider_name]

        # Execute
        response = await self._execute_with_retry(provider, request)

        # Clean reasoning tags if present
        clean_content, reasoning = self.extract_clean_code_and_reasoning(response.content)

        # We don't overwrite response.content with just code yet unless we are sure it's needed,
        # but the prompt asked for a self-healing extraction. We will update the response.
        response.content = clean_content

        # If there's an existing reasoning trace, append or just set it
        if reasoning:
            response.reasoning_trace = reasoning

        return response

    async def get_health_status(self) -> Dict[str, bool]:
        """Returns health status for all registered providers."""
        status = {}
        for name, provider in self.providers.items():
            status[name] = await provider.health_check()
        return status
