# Architecture Decision Record (ADR): Multi-Engine & Camera Perspectives

## Context
Standard educational platforms often lock into a single visual modality (e.g., exclusively 2D vector, or exclusively static 3D). This leads to perceptual habituation; after 10 hours, the brain stops noticing the novelty of the visual representation, which reduces engagement.

## Decision
We will employ a **Multi-Renderer Orchestrator** supporting diverse execution targets and camera rigs, allowing us to contextually switch representations based on the concept and user preference.

### The 4 Render Pipelines
1. **Interactive WebGL / Three.js 3D Stage**:
   - Supports First-Person POV (riding inside the data).
   - Supports Third-Person Tracking (following an algorithm pointer).
   - Supports Isometric Diorama (broad system overview).
2. **HTML5 Hybrid Canvas**:
   - Mixes SVG for crisp mathematical vectors and `<canvas>` for 16-bit retro pixel shaders.
3. **Manim Community Video**:
   - Standard 3B1B-style animated MP4s, overlayed with synchronized DOM pause states for micro-interactions.
4. **Blender 3D (`bpy`)**:
   - Programmatically generated high-fidelity cinematic 3D renders using Python via the local Blender CLI.

## Consequences
- Requires a modular frontend architecture (`ModularStudioViewport`) capable of dynamic component hot-swapping.
- Prevents perceptual fatigue by regularly morphing the visual representation format while maintaining the same underlying abstract mathematical/computer science concepts.
