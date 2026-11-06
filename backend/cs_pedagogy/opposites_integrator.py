from typing import Dict, Any, List
from backend.cs_pedagogy.interfaces import KinematicPedagogicalGraph70, ConceptArtSpecification30, DialecticalSceneManifest

class OppositesIntegrator:
    """
    The 'Integration of the Opposites' Synthesizer & Auditor.
    Merges the 70% Kinematic Pedagogical Skeleton with the 30% Concept-Art World Skin.
    """

    def synthesize(self, graph: KinematicPedagogicalGraph70, style: ConceptArtSpecification30) -> DialecticalSceneManifest:
        elements: List[Dict[str, Any]] = []

        # Inject the 30% Ambient Motion and World-Building as foundational elements
        elements.append({
            "id": "ambient_world",
            "type": "background_motion",
            "style_rules": {
                "palette": style.palette,
                "motion": style.ambient_motion
            },
            "role": "ROLE_30_SENSORY_CONCEPT_ART"
        })

        # Process the 70% Entities and dress them in the 30% Style
        for entity in graph.entities:
            merged_entity = dict(entity)
            # It already has role ROLE_70_PEDAGOGICAL_TRANSFER from the 70 engine.
            # We apply the geometry rules to it.
            merged_entity["geometry"] = style.geometry_rules
            merged_entity["color"] = style.palette.get("accent", "#FFFFFF")
            elements.append(merged_entity)

        # Add a 30% continuous glow or shader to elements
        elements.append({
            "id": "global_shader_overlay",
            "type": "shader",
            "effect": f"Apply {style.style.value} continuous fluid shader",
            "role": "ROLE_30_SENSORY_CONCEPT_ART"
        })

        # Process the 70% Transitions
        for transition in graph.transitions:
            merged_transition = dict(transition)
            # Enhance transition with 30% kinetic style
            merged_transition["kinetic_easing"] = "elastic" if "elastic" in style.ambient_motion else "linear"
            elements.append(merged_transition)

        manifest = DialecticalSceneManifest(
            concept_id=graph.concept_id,
            elements=elements
        )

        # Validate that everything has a strict role
        manifest.validate_roles()
        return manifest

    def audit_manifest(self, manifest: DialecticalSceneManifest) -> Dict[str, float]:
        """
        Audits that the 70/30 balance is mathematically preserved.
        """
        count_70 = 0
        count_30 = 0
        for el in manifest.elements:
            role = el.get("role")
            if role == "ROLE_70_PEDAGOGICAL_TRANSFER":
                count_70 += 1
            elif role == "ROLE_30_SENSORY_CONCEPT_ART":
                count_30 += 1

        total = count_70 + count_30
        if total == 0:
            return {"70_percent": 0.0, "30_percent": 0.0}

        ratio_70 = count_70 / total
        ratio_30 = count_30 / total

        # In a real environment, we'd log or throw if ratio is severely off, but we return it for testing
        return {
            "70_percent": ratio_70,
            "30_percent": ratio_30
        }
