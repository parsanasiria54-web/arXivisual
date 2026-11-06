# Frontend Architecture: Chameleon Theming & Micro-Triggers

## The Chameleon Adaptive UI
A static UI environment feels like a classroom. To create a multi-dimensional studio, the overarching container (`ModularStudioViewport`) dynamically morphs its CSS classes based on the current context.

### Theme Dimensions
- **Global Theme Shell**: Backgrounds and fonts change radically (`THEME_OBSIDIAN_DARK`, `THEME_CYBER_GRID`).
- **Concept-Art Paradigm**: A drop-down that hot-swaps the visual styling of the inner canvas content (e.g., from `WESTERN_GRAPHIC_VECTOR` to `VOXEL_3D_CONSTRUCT`).

## Implementing the 10% Micro-Trigger
In `Html5HybridViewport` and `ManimSyncedViewport`, we implement state machines that simulate these zero-stress mechanics:
- An SVG element with an `onClick` handler that steps a `bundleCount` state integer forward, visually scaling a circle. There is no timer, no score penalty for clicking slowly, and no way to "fail." It exists purely for physical engagement at the exact moment a conceptual threshold is crossed.
- A video overlay that pauses the stream and awaits user confirmation to proceed, simulating an interactive stopping point.
