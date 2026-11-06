# Word Boundaries & Audio Math: The Engineering Mechanics

To make Audio the Master Clock, you cannot simply say `duration = 5 seconds`. You need extreme precision, down to the frame and millisecond, and ideally at the word level to sync subtitles or highlight specific formulas on screen as they are spoken.

## Extracting Millisecond Boundaries
Neural TTS endpoints (like Microsoft Edge) can return a stream of events alongside the audio bytes.
1. We intercept the `AudioBoundary` events.
2. We map the event ticks (often in 100-nanosecond units) to standard seconds.
3. We store this in the `AudioSyncManifest`.

## Raw Audio Header Math (Zero-Dependency)
In scenarios where we fallback to offline or gTTS, we don't have word boundaries. But we still *must* know the absolute duration to feed the Manim `wait()` function.

Instead of relying on heavy libraries like `ffmpeg` or `librosa` inside a fast API endpoint, we can mathematically calculate duration by parsing the raw WAV header.

A WAV file starts with a RIFF header.
1. Byte 24-27: Sample Rate (e.g., 44100 Hz)
2. Byte 34-35: Bits per sample (e.g., 16)
3. Byte 22-23: Number of channels (e.g., 1 or 2)
4. Then we find the `data` chunk and read its size.

`Duration = DataSize / (SampleRate * Channels * (BitsPerSample / 8))`

This gives us deterministic float precision in less than a millisecond without installing any external binary dependencies.

## Orchestration & Caching
Because developers run Manim scripts hundreds of times while debugging visual positioning, we cannot hit the TTS endpoint every time. The `SyncOrchestrator` implements a SHA-256 hash of `(text, language, voice, speed, provider)`. If the hash matches a local cache, we instantly yield the cached audio and `AudioSyncManifest`, dropping video generation latency to zero.
