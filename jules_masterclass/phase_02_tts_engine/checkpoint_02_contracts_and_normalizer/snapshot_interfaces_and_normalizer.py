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
import re

class LanguageDetector:
    """
    Detects language (English or Persian) and normalizes CS/Math terminology for TTS.
    """

    @staticmethod
    def detect_language(text: str) -> str:
        """
        Deterministically detects if the text is primarily Persian or English.
        Uses character ranges.
        """
        # Persian/Arabic unicode ranges: \u0600-\u06FF, \u0750-\u077F, \u08A0-\u08FF, \uFB50-\uFDFF, \uFE70-\uFEFF
        fa_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        fa_chars = len(fa_pattern.findall(text))
        en_chars = len(re.findall(r'[a-zA-Z]', text))

        return "fa" if fa_chars > en_chars else "en"

    @staticmethod
    def normalize_math_and_cs(text: str, language: str) -> str:
        """
        Normalizes Math (LaTeX) and CS terms for natural pronunciation.
        """
        normalized = text

        # Strip simple inline code ticks
        normalized = re.sub(r'`([^`]+)`', r'\1', normalized)

        if language == "en":
            # O(n) notation
            normalized = re.sub(r'O\(([a-zA-Z0-9\s\+\-\*]+)\)', r'O of \1', normalized)
            normalized = re.sub(r'O\(n \\log n\)', 'O of n log n', normalized)
            # Latex stripping (very basic for now)
            normalized = normalized.replace('$', '')
            normalized = normalized.replace('\\log', 'log')
            normalized = normalized.replace('\\frac', 'fraction')

            # CS acronyms (Add spaces so TTS reads as letters if needed, though most modern TTS handles them)
            # For this simple mock, we'll replace known symbols
            normalized = normalized.replace('/', ' slash ')

        elif language == "fa":
            # O(n) in Persian context
            normalized = re.sub(r'O\(([a-zA-Z0-9\s\+\-\*]+)\)', r'اوو ی \1', normalized)
            normalized = re.sub(r'O\(n \\log n\)', 'اوو ی اِن لاگ اِن', normalized)

            # Basic math symbols to Persian
            normalized = normalized.replace('+', ' به علاوه ')
            normalized = normalized.replace('-', ' منهای ')
            normalized = normalized.replace('=', ' مساوی ')

            normalized = normalized.replace('$', '')
            normalized = normalized.replace('\\log', 'لاگ')
            normalized = normalized.replace('\\frac', 'کسر')

            normalized = normalized.replace('/', ' اسلش ')

        # Cleanup extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        return normalized

    @classmethod
    def process(cls, text: str) -> tuple[str, str]:
        """
        Returns (detected_language, normalized_text)
        """
        lang = cls.detect_language(text)
        norm_text = cls.normalize_math_and_cs(text, lang)
        return lang, norm_text
