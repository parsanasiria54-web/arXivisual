# Headless Audio Testing in CI Environments

A major problem with audio pipelines is that they often rely on OS-level soundcards, hardware ALSA/PulseAudio dependencies, or expensive network endpoints. If we run an edge neural TTS generator inside a GitHub Action, tests become flaky due to network timeouts, or they fail because standard Linux runners lack audio drivers.

## The Headless Deterministic Solution
To solve this, our architecture leverages the `LocalOfflineProvider` combined with a deterministic "mock mode".

1. **No External Network**: The offline provider intercepts TTS requests inside the test suite and never fires an HTTP call.
2. **Silent WAV Generation**: It generates real byte-for-byte correct `.wav` files using hardcoded RIFF/WAVE headers and an empty data chunk. This means downstream tools (like Manim's rendering pipeline) believe a real audio file exists and can parse its headers successfully.
3. **Deterministic Timings**: Instead of using real neural timing, the offline provider mathematically calculates a fake duration strictly based on string length (e.g. `len(text) * 0.05`). This means `assert duration == 1.2` will always pass deterministically, regardless of CPU speed.

By implementing this, the entire `SyncOrchestrator` logic can be perfectly tested in under a second inside an ephemeral CI container.
