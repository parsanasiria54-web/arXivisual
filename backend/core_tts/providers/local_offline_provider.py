from typing import List, Dict
import asyncio
from backend.core_tts.interfaces import TTSProvider, TTSRequest, TTSAudioSegment, AudioSyncManifest

class LocalOfflineProvider(TTSProvider):
    """
    Offline TTS adapter (e.g. Piper, Kokoro).
    Can generate deterministic silent/tone WAV files for headless CI testing.
    """

    async def get_voices(self) -> dict:
        return {
            "en": ["offline-en-mock"],
            "fa": ["offline-fa-mock"]
        }

    async def synthesize(self, request: TTSRequest, output_path: str) -> TTSAudioSegment:
        # Simulate local synthesis
        await asyncio.sleep(0.01)

        # Write dummy WAV bytes for CI
        with open(output_path, "wb") as f:
            f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00")

        # Deterministic duration based strictly on string length for tests
        duration = len(request.text) * 0.05

        manifest = AudioSyncManifest(
            duration_seconds=duration,
            word_boundaries=[],
            manim_wait_timings={"ci_scene": duration}
        )

        return TTSAudioSegment(
            file_path=output_path,
            manifest=manifest,
            metadata={"provider": "local_mock", "ci_mode": True}
        )
