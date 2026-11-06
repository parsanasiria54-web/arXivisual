from typing import List, Dict
import asyncio
from backend.core_tts.interfaces import TTSProvider, TTSRequest, TTSAudioSegment, AudioSyncManifest

class GTTSFallbackProvider(TTSProvider):
    """
    Lightweight fallback using gTTS. Does not natively provide word boundaries easily,
    so we calculate approximate durations.
    """

    async def get_voices(self) -> dict:
        return {
            "en": ["gtts-en-default"],
            "fa": ["gtts-fa-default"]
        }

    async def synthesize(self, request: TTSRequest, output_path: str) -> TTSAudioSegment:
        # Simulate gtts usage
        await asyncio.sleep(0.05)

        # Write dummy WAV bytes
        with open(output_path, "wb") as f:
            f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00")

        # Mock calculation: 150 words per minute -> 2.5 words per second
        words = request.text.split()
        estimated_duration = (len(words) / 2.5) / request.speed

        manifest = AudioSyncManifest(
            duration_seconds=estimated_duration,
            word_boundaries=[], # No precise boundaries available natively
            manim_wait_timings={"fallback_scene": estimated_duration}
        )

        return TTSAudioSegment(
            file_path=output_path,
            manifest=manifest,
            metadata={"provider": "gtts", "fallback": True}
        )
