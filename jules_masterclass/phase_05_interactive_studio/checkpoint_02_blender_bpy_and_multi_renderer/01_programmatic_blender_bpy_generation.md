# Programmatic Blender BPY Generation

## Core Challenge
How do we convert abstract AI-generated pedagogical scene plans into high-fidelity 3D animations without manual human 3D modeling?

## Solution: The `blender_bridge.py` Pipeline
We use Blender's Headless Python API (`bpy`). The backend architecture is responsible for generating deterministic python scripts that, when executed by `blender --background --python script.py`, yield identical 3D scenes.

### Process
1. **Manifest Intake**: The LLM outputs a structured JSON "scene manifest" containing definitions for objects, cameras, and lights.
2. **Script Generation**: `BlenderBridge.generate_bpy_script()` maps this JSON to valid `bpy` operations (e.g., `bpy.ops.mesh.primitive_cube_add`).
3. **Deterministic Assembly**: We explicitly clear the default scene (`bpy.ops.wm.read_factory_settings(use_empty=True)`) at the start of every generated script to prevent state leakage and ensure deterministic output.
4. **Execution Target**: This script is passed to the Blender CLI (if available in the environment) to render out the frames or construct `.blend` files for interactive viewing.

This completely automates the 3D pipeline, turning descriptive scene data into physical 3D meshes and cinematic rigs.
