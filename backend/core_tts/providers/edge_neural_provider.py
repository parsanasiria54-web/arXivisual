from typing import List, Dict
import asyncio
from backend.core_tts.interfaces import TTSProvider, TTSRequest, TTSAudioSegment, AudioSyncManifest, WordBoundaryTimestamp

class EdgeNeuralProvider(TTSProvider):
    """
    Microsoft Edge Neural TTS.
    Simulates fetching word-boundary subtitle extraction for Manim.
    """

    VOICES = {
        "en": ["en-US-AriaNeural", "en-US-GuyNeural"],
        "fa": ["fa-IR-FaridNeural", "fa-IR-DilaraNeural"]
    }

    async def get_voices(self) -> dict:
        return self.VOICES

    async def synthesize(self, request: TTSRequest, output_path: str) -> TTSAudioSegment:
        # Simulate network delay and audio generation
        await asyncio.sleep(0.1)

        # Write dummy WAV bytes
        with open(output_path, "wb") as f:
            f.write(b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00")

        # Simulate word boundaries
        words = request.text.split()
        boundaries = []
        current_time = 0.0

        for w in words:
            # mock duration 0.3s per word based on speed
            duration = 0.3 / request.speed
            boundaries.append(
                WordBoundaryTimestamp(
                    word=w,
                    start_time=current_time,
                    end_time=current_time + duration
                )
            )
            current_time += duration

        manifest = AudioSyncManifest(
            duration_seconds=current_time,
            word_boundaries=boundaries,
            manim_wait_timings={"scene_1": current_time}
        )

        return TTSAudioSegment(
            file_path=output_path,
            manifest=manifest,
            metadata={"provider": "edge", "voice_id": request.voice_id}
        )
