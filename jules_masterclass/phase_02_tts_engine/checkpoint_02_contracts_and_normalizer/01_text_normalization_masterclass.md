# Text Normalization Masterclass: Handling Mixed-Script and CS Notations

When feeding raw text from an educational context (like Manim code or LaTeX-heavy markdown) to a TTS engine, the results are often disastrous. TTS engines read punctuation and syntax literally if they don't have specialized context models.

## The Problem
Consider the text: `The time complexity is $O(V + E)$ where $V$ is vertices.`
A naive TTS will read this as: "The time complexity is dollar sign capital O open parenthesis capital V plus capital E close parenthesis dollar sign where dollar sign capital V dollar sign is vertices."

This shatters the educational immersion.

## The Solution: Deterministic Pre-processing (Normalization)
Before hitting the synthesis endpoint, we must mutate the string.

### 1. Script Detection
Because we are building a bilingual system, the normalizer must know the target language context to choose the right phonetic equivalents.
We use character-range detection (`\u0600-\u06FF` etc. for Persian) to deterministically route the text. If Persian characters outnumber English ones, we assume a Persian sentence that might have embedded English/Math notations.

### 2. Regex and AST Replacements
We use Regex to capture common mathematical patterns:
*   `O(n \log n)` -> "O of n log n" (English) or "اوو ی اِن لاگ اِن" (Persian)
*   `$O(V + E)$` -> "O of V plus E"

## Implementation Notes
The `LanguageDetector` class handles both detection and normalization. It acts as a safety middleware sitting between the raw Manim voiceover request and the actual TTS provider logic. By ensuring all LaTeX ($) is stripped and math acronyms are expanded, we guarantee smooth natural playback.
