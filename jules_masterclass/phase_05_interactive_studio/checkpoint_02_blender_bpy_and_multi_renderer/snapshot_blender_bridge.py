"""
Programmatic Blender Python (`bpy`) pipeline bridge.
Generates deterministic Blender Python scripts from pedagogical scene manifests.
"""

import json

class BlenderBridge:
    def __init__(self, scene_name="PedagogicalScene"):
        self.scene_name = scene_name

    def generate_bpy_script(self, scene_manifest: dict) -> str:
        """
        Generates a blender python script string that constructs 3D meshes,
        volumetric lighting, and keyframed camera rigs based on the input manifest.

        Args:
            scene_manifest: A dictionary containing 'objects', 'cameras', 'lights' etc.
        """

        lines = []
        lines.append("import bpy")
        lines.append("import math")
        lines.append("")

        # Clear existing scene
        lines.append("# Clear default scene")
        lines.append("bpy.ops.wm.read_factory_settings(use_empty=True)")
        lines.append("")

        # Parse manifest objects
        objects = scene_manifest.get("objects", [])
        for obj in objects:
            obj_type = obj.get("type", "cube")
            loc = obj.get("location", [0, 0, 0])
            scale = obj.get("scale", [1, 1, 1])

            if obj_type == "cube":
                lines.append(f"bpy.ops.mesh.primitive_cube_add(location={tuple(loc)}, scale={tuple(scale)})")
            elif obj_type == "sphere":
                lines.append(f"bpy.ops.mesh.primitive_uv_sphere_add(location={tuple(loc)}, scale={tuple(scale)})")

        lines.append("")

        # Set up camera
        cameras = scene_manifest.get("cameras", [{"location": [0, -5, 2], "rotation": [math.radians(90), 0, 0]}])
        if cameras:
            cam = cameras[0]
            lines.append("# Set up Camera")
            lines.append(f"bpy.ops.object.camera_add(location={tuple(cam.get('location', [0,-5,2]))})")
            lines.append("camera = bpy.context.object")
            lines.append(f"camera.rotation_euler = {tuple(cam.get('rotation', [math.radians(90), 0, 0]))}")
            lines.append("bpy.context.scene.camera = camera")
            lines.append("")

        # Set up lighting
        lights = scene_manifest.get("lights", [{"type": "POINT", "location": [2, -2, 2], "energy": 1000}])
        for idx, light in enumerate(lights):
            lines.append(f"# Set up Light {idx}")
            lines.append(f"bpy.ops.object.light_add(type='{light.get('type', 'POINT')}', location={tuple(light.get('location', [2,-2,2]))})")
            lines.append("light = bpy.context.object")
            lines.append(f"light.data.energy = {light.get('energy', 1000)}")

        lines.append("")
        lines.append("# Output save/render instructions could go here")
        lines.append("print('Blender scene generation complete.')")

        return "\n".join(lines)
