# Architecture Decision Record: Bilingual TTS & Normalization

**Date:** 2024-XX-XX
**Status:** Accepted
**Context:** The system requires a highly robust Text-to-Speech (TTS) engine for generating voiceovers for Manim educational videos. The content frequently mixes English and Persian/Farsi, and includes heavy Computer Science and Mathematical notation (LaTeX, acronyms).

## Decisions

### 1. Hybrid TTS Adapters (Online + Offline)
We will implement an adapter pattern with multiple providers:
*   **Edge Neural Provider:** Primary engine using free, high-quality Microsoft Edge Neural TTS endpoints. It supports both English (`en-US-AriaNeural`, `en-US-GuyNeural`) and Persian (`fa-IR-FaridNeural`, `fa-IR-DilaraNeural`). Crucially, it provides word-level timing/subtitle extraction, satisfying the "Audio-as-Master-Clock" requirement.
*   **gTTS Fallback:** A lightweight, highly available fallback if neural endpoints fail.
*   **Local Offline Provider:** Designed for CI/CD, local development, or environments without external network access. It uses local CLI/HTTP engines or a deterministic silent/tone generator to ensure tests run reliably without network flakiness.

### 2. Mixed-Script Handling & Computer Science Normalization
Mathematical equations (e.g., `$O(n \log n)$`) and CS acronyms (e.g., `BFS`, `JSON`) are poorly handled by raw TTS engines, leading to bizarre pronunciations (e.g., "dollar backslash oh...").

We introduce a dedicated **Language Detector & Normalizer** (`language_detector.py`):
*   **Script Detection:** It will analyze character ranges deterministically to identify the primary language context (LTR English vs RTL Persian).
*   **Regex/AST Normalization:** It will strip or convert LaTeX and CS notation into phonetically safe strings *before* hitting the TTS engine. For example, `$O(n \log n)$` becomes "O of n log n" in English context, or its Persian phonetic equivalent in a Persian context.

### Consequences
*   **Positive:** Highly resilient architecture that degrades gracefully from high-quality neural voice down to local silent generation for CI.
*   **Positive:** Accurate pronunciation of CS terminology drastically improves the educational quality of the final videos.
*   **Negative:** Managing word boundaries across different providers requires a robust synchronization orchestrator, as fallbacks like gTTS do not natively provide millisecond-level word timing.
