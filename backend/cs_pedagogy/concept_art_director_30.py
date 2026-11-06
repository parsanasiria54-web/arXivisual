from typing import Dict, Any, List
from backend.cs_pedagogy.interfaces import StyleParadigmEnum, ConceptArtSpecification30

class ConceptArtDirector30:
    """
    The 30% Academic Concept-Art & Style Rotation Director.
    Exclusively responsible for Continuous Sensory Fluidity, World-Building Concept Design, and Novelty Rotation.
    """

    def __init__(self):
        self.style_history: List[StyleParadigmEnum] = []
        self.styles = list(StyleParadigmEnum)

    def _get_next_style(self) -> StyleParadigmEnum:
        """Ensures non-repeating style rotation across concept sequences."""
        available_styles = [s for s in self.styles if not (self.style_history and s == self.style_history[-1])]
        # Simple round-robin from available styles for predictability in rotation
        next_style = available_styles[0]
        self.style_history.append(next_style)
        return next_style

    def generate_style_specification(self) -> ConceptArtSpecification30:
        style = self._get_next_style()

        if style == StyleParadigmEnum.DARK_MANHWA_ABYSS:
            palette = {"background": "#07090E", "accent": "#00F0FF", "shadow": "#8A2BE2"}
            geom = {"stroke_weight": 2.0, "corner_radius": 0.0, "glow_radius": 5.0}
            motion = "High-velocity slash/surge transitions with ambient volumetric void glow"

        elif style == StyleParadigmEnum.WESTERN_GRAPHIC_VECTOR:
            palette = {"background": "#FFFFFF", "accent": "#FF4500", "outline": "#000000"}
            geom = {"stroke_weight": 5.0, "corner_radius": 0.5, "glow_radius": 0.0}
            motion = "Snappy elastic squash-and-stretch morphing with continuous vector pulsing"

        elif style == StyleParadigmEnum.RETRO_16BIT_GRID:
            palette = {"background": "#0000AA", "accent": "#FFAA00", "grid": "#55FFFF"}
            geom = {"stroke_weight": 1.0, "corner_radius": 0.0, "pixelated": True}
            motion = "Quantized grid-snapping movement and discrete pixel-block shimmering"

        elif style == StyleParadigmEnum.VOXEL_3D_CONSTRUCT:
            palette = {"background": "#E0E0E0", "primary_block": "#4CAF50", "shadow": "#9E9E9E"}
            geom = {"stroke_weight": 0.5, "isometric": True, "depth": 2.0}
            motion = "Tactile block-stacking assembly with continuous soft shadow rotation"

        elif style == StyleParadigmEnum.HARD_SCIFI_TELEMETRY:
            palette = {"background": "#001100", "wireframe": "#00FF00", "highlight": "#00FFFF"}
            geom = {"stroke_weight": 1.0, "corner_radius": 0.2, "opacity": 0.7}
            motion = "Wireframe holographic projections with rotating orbital target rings"

        else:
            raise ValueError(f"Unknown style: {style}")

        return ConceptArtSpecification30(
            style=style,
            palette=palette,
            geometry_rules=geom,
            ambient_motion=motion
        )
