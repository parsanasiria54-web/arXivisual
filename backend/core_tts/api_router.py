from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import tempfile
import os

from backend.core_tts.interfaces import TTSRequest, TTSAudioSegment
from backend.core_tts.language_detector import LanguageDetector
from backend.core_tts.sync_orchestrator import SyncOrchestrator
from backend.core_tts.providers.edge_neural_provider import EdgeNeuralProvider
from backend.core_tts.providers.gtts_fallback_provider import GTTSFallbackProvider
from backend.core_tts.providers.local_offline_provider import LocalOfflineProvider

router = APIRouter(prefix="/api/v1/tts", tags=["tts"])

PROVIDERS = {
    "edge": EdgeNeuralProvider(),
    "gtts": GTTSFallbackProvider(),
    "local": LocalOfflineProvider()
}

@router.get("/voices")
async def get_voices():
    """
    Returns available voices from all configured providers.
    """
    voices_catalog = {}
    for provider_name, provider_inst in PROVIDERS.items():
        voices_catalog[provider_name] = await provider_inst.get_voices()
    return voices_catalog

@router.post("/synthesize", response_model=TTSAudioSegment)
async def synthesize_speech(request: TTSRequest):
    """
    Normalizes text, routes to requested provider, and returns audio + timing manifest.
    """
    if request.provider not in PROVIDERS:
        raise HTTPException(status_code=400, detail=f"Provider '{request.provider}' not supported.")

    # 1. Normalize and detect language
    detected_lang, norm_text = LanguageDetector.process(request.text)

    # Overwrite request text with normalized text and set detected language if not forced
    request.text = norm_text
    request.language = detected_lang

    # 2. Prepare orchestrator
    orchestrator = SyncOrchestrator(provider=PROVIDERS[request.provider])

    # 3. Create temp output file path
    temp_fd, output_path = tempfile.mkstemp(suffix=".wav")
    os.close(temp_fd) # Close file descriptor, let provider handle writing

    # 4. Generate
    try:
        segment = await orchestrator.process_and_sync(request, output_path)
        return segment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
