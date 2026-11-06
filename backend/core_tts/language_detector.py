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
