# Architecture Decision Record (ADR): Per-Concept Style Imprinting

## Context
Adult ADHD learners suffer from rapid habituation to visual stimuli. If the entire course on Computer Science is taught using the same color palette, geometry, and ambient motion, the learner's brain will start ignoring the visual channel, drastically reducing the retention of abstract concepts.

## Decision
We enforce a mandatory **Per-Concept Aesthetic Rotation**. Each atomic concept MUST be stamped into the learner's memory with its own distinct Concept-Art Paradigm. Furthermore, consecutive concepts MUST switch styles.

## Paradigms Implemented
We implemented 5 distinct, mathematically parameterized Manim Concept-Art Paradigms:
1. `DARK_MANHWA_ABYSS`: Deep obsidian void (`#07090E`), angular geometry, glowing cyan (`#00F0FF`) & shadow-violet (`#8A2BE2`) energy auras. (Inspired by *Solo Leveling*)
2. `WESTERN_GRAPHIC_VECTOR`: Bold cel-shaded outlines, high-contrast emerald/charcoal/amber vector cores, snappy elastic squash-and-stretch morphing. (Inspired by *Ben 10*)
3. `RETRO_16BIT_GRID`: Quantized grid-snapping movement, discrete pixel-block containers, vibrant arcade palette. (Inspired by classic 2D platformer physics like *Super Mario*)
4. `VOXEL_3D_CONSTRUCT`: Isometric/3D cubic primitives, tactile block-stacking assembly, structural depth. (Inspired by *Minecraft*)
5. `HARD_SCIFI_TELEMETRY`: Wireframe holographic projections, orbital target rings, phosphor amber/teal telemetry aesthetics. (Inspired by *Star Wars* diegetic schematics)

## Consequences
- **Positive:** Concepts are highly distinguished in memory. Sensory habituation is prevented.
- **Negative:** Increased complexity in the synthesis step, requiring rigorous separation between style-agnostic mechanics (70%) and aesthetic application (30%).
