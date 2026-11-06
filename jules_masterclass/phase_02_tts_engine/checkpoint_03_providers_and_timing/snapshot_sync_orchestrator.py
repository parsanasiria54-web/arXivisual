import hashlib
from backend.core_tts.interfaces import TTSProvider, TTSRequest, TTSAudioSegment

class SyncOrchestrator:
    """
    Coordinates TTS synthesis, calculates audio duration/frames,
    and handles hashing to avoid redundant regeneration.
    """

    def __init__(self, provider: TTSProvider):
        self.provider = provider

    def generate_hash(self, request: TTSRequest) -> str:
        """
        Generate a SHA-256 hash for caching based on request attributes.
        """
        raw = f"{request.text}|{request.language}|{request.voice_id}|{request.speed}|{request.provider}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    async def process_and_sync(self, request: TTSRequest, output_path: str) -> TTSAudioSegment:
        """
        Synthesize text and update manifest with hashing and exact wait timings.
        """
        segment = await self.provider.synthesize(request, output_path)

        # Inject caching hash
        cache_hash = self.generate_hash(request)
        segment.manifest.caching_hash = cache_hash

        # Calculate exactly how long Manim should wait (assume base duration is enough if no overlap logic needed)
        segment.manifest.manim_wait_timings["auto_wait"] = segment.manifest.duration_seconds

        return segment
