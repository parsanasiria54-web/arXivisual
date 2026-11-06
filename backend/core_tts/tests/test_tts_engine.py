import pytest
import os
from backend.core_tts.language_detector import LanguageDetector
from backend.core_tts.interfaces import TTSRequest
from backend.core_tts.providers.local_offline_provider import LocalOfflineProvider
from backend.core_tts.sync_orchestrator import SyncOrchestrator

def test_language_detection():
    en_text = "This is a simple English sentence."
    fa_text = "این یک جمله ساده فارسی است."
    mixed_text = "The complexity is اوو ی اِن"

    assert LanguageDetector.detect_language(en_text) == "en"
    assert LanguageDetector.detect_language(fa_text) == "fa"
    # Mixed goes by character count, the en chars dominate here
    assert LanguageDetector.detect_language(mixed_text) == "en"

def test_math_normalization_en():
    raw = "The time complexity is $O(n \\log n)$"
    lang, norm = LanguageDetector.process(raw)
    assert lang == "en"
    assert "O of n log n" in norm
    assert "$" not in norm

def test_math_normalization_fa():
    raw = "زمان اجرا $O(n \\log n)$ است."
    lang, norm = LanguageDetector.process(raw)
    assert lang == "fa"
    assert "اوو ی اِن لاگ اِن" in norm
    assert "$" not in norm

@pytest.mark.asyncio
async def test_offline_provider_and_orchestrator():
    provider = LocalOfflineProvider()
    orchestrator = SyncOrchestrator(provider)

    request = TTSRequest(text="Testing pipeline.", provider="local")
    output_path = "test_output.wav"

    segment = await orchestrator.process_and_sync(request, output_path)

    assert os.path.exists(segment.file_path)
    assert segment.manifest.duration_seconds > 0
    assert segment.manifest.caching_hash != ""
    assert segment.metadata["ci_mode"] is True

    # Cleanup
    if os.path.exists(output_path):
        os.remove(output_path)
