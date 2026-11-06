# Masterclass: Procedural Concept Art in Manim

## 1. The Anti-Clipart Rule
Standard educational videos paste vector clipart onto the screen. This shatters immersion.
In this engine, we strictly forbid clipart. Everything must be procedurally generated via Manim shaders, stroke profiles, volumetric glows, and continuous 30% ambient motion.

## 2. Translating Styles to Mathematics
When the `ConceptArtDirector30` generates a specification, it translates high-level aesthetics into mathematical parameters:

- **DARK_MANHWA_ABYSS:**
  - `stroke_weight`: 2.0
  - `glow_radius`: 5.0
  - Colors: `#07090E` (Void), `#00F0FF` (Cyan Aura)

- **WESTERN_GRAPHIC_VECTOR:**
  - `stroke_weight`: 5.0 (Bold cel-shaded)
  - `corner_radius`: 0.5
  - Squash-and-stretch morphing applied to kinetic easing.

## 3. The Synthesis
The `OppositesIntegrator` takes the rigid 70% pedagogical state machine and injects the 30% concept art.
It ensures that a foundational "ambient world" element is always present, preventing dead frames.
It also applies global shader overlays.
Every single element resulting from this merge is strictly tagged `ROLE_70_PEDAGOGICAL_TRANSFER` or `ROLE_30_SENSORY_CONCEPT_ART`, ensuring zero ambiguity.
