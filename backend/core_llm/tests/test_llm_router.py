import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.core_llm.interfaces import LLMRequest, LLMResponse, TokenUsage
from backend.core_llm.router_service import RouterService
from backend.core_llm.providers.ollama_provider import OllamaProvider
from backend.core_llm.providers.cloud_openai_compat import CloudOpenAICompatProvider

@pytest.fixture
def sample_request():
    return LLMRequest(
        messages=[{"role": "user", "content": "Write a python script"}],
        model="gpt-oss:20b"
    )

def test_extract_clean_code_and_reasoning():
    service = RouterService()

    # Test 1: No reasoning tags
    text1 = "```python\nprint('hello')\n```"
    clean, reasoning = service.extract_clean_code_and_reasoning(text1)
    assert reasoning is None
    assert clean == "print('hello')"

    # Test 2: With <think> tags
    text2 = "<think>I need to write a script.</think>\n```python\nprint('hello')\n```"
    clean, reasoning = service.extract_clean_code_and_reasoning(text2)
    assert reasoning == "I need to write a script."
    assert clean == "print('hello')"

@pytest.mark.asyncio
@patch('httpx.AsyncClient.post')
async def test_ollama_provider_generate(mock_post, sample_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Ollama response"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    }
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    provider = OllamaProvider()
    response = await provider.generate(sample_request)

    assert isinstance(response, LLMResponse)
    assert response.content == "Ollama response"
    assert response.model_used == "gpt-oss:20b"
    assert response.usage.total_tokens == 30

@pytest.mark.asyncio
async def test_router_service_routing(sample_request):
    service = RouterService()

    # Mock the execute method directly to bypass HTTP
    mock_resp = LLMResponse(
        content="<think>Hmm</think>```json\n{\"key\":\"val\"}\n```",
        model_used="test-model",
        usage=TokenUsage()
    )

    mock_execute = AsyncMock(return_value=mock_resp)
    service._execute_with_retry = mock_execute

    response = await service.route_request("ollama", sample_request)

    assert mock_execute.called
    assert response.reasoning_trace == "Hmm"
    assert response.content == "{\"key\":\"val\"}"

@pytest.mark.asyncio
async def test_router_service_retry_logic(sample_request):
    service = RouterService()

    # Make a dummy provider that fails twice then succeeds
    mock_provider = AsyncMock()
    mock_provider.generate.side_effect = [
        Exception("Timeout 1"),
        Exception("Timeout 2"),
        LLMResponse(content="Success", model_used="test", usage=TokenUsage())
    ]

    # Temporarily replace asyncio.sleep to not wait during tests
    with patch('asyncio.sleep', AsyncMock()):
        response = await service._execute_with_retry(mock_provider, sample_request, max_retries=3)

    assert response.content == "Success"
    assert mock_provider.generate.call_count == 3
