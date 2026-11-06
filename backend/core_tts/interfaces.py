from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class TTSRequest(BaseModel):
    text: str = Field(..., description="The input text to synthesize.")
    language: str = Field(default="en", description="Target language ('en' or 'fa').")
    voice_id: str = Field(default="", description="The specific voice identifier to use.")
    speed: float = Field(default=1.0, description="Speech rate/speed.")
    provider: str = Field(default="edge", description="Provider choice (edge, gtts, local).")

class WordBoundaryTimestamp(BaseModel):
    word: str
    start_time: float = Field(..., description="Start time in seconds.")
    end_time: float = Field(..., description="End time in seconds.")

class AudioSyncManifest(BaseModel):
    duration_seconds: float = Field(..., description="Exact duration of the generated audio.")
    word_boundaries: List[WordBoundaryTimestamp] = Field(default_factory=list, description="Word level boundaries.")
    manim_wait_timings: Dict[str, float] = Field(default_factory=dict, description="Recommended wait times for Manim scenes.")
    caching_hash: str = Field(default="", description="SHA-256 hash for caching.")

class TTSAudioSegment(BaseModel):
    file_path: str = Field(..., description="Local path to the synthesized audio file.")
    manifest: AudioSyncManifest = Field(..., description="Synchronization manifest for this audio.")
    metadata: dict = Field(default_factory=dict, description="Any additional provider-specific metadata.")

class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, request: TTSRequest, output_path: str) -> TTSAudioSegment:
        """
        Synthesize text into speech and return an audio segment with timing manifest.
        """
        pass

    @abstractmethod
    async def get_voices(self) -> dict:
        """
        Return available voices grouped by language.
        """
        pass
