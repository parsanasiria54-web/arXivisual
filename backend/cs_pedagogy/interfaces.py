from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class StyleParadigmEnum(str, Enum):
    DARK_MANHWA_ABYSS = "DARK_MANHWA_ABYSS"
    WESTERN_GRAPHIC_VECTOR = "WESTERN_GRAPHIC_VECTOR"
    RETRO_16BIT_GRID = "RETRO_16BIT_GRID"
    VOXEL_3D_CONSTRUCT = "VOXEL_3D_CONSTRUCT"
    HARD_SCIFI_TELEMETRY = "HARD_SCIFI_TELEMETRY"

class VisualMemoryAnchor(BaseModel):
    id: str = Field(description="Unique ID for this memory anchor")
    description: str = Field(description="Description of the visual memory anchor")

class KinematicPedagogicalGraph70(BaseModel):
    concept_id: str = Field(description="The ID of the concept being taught")
    entities: List[Dict[str, Any]] = Field(default_factory=list, description="Style-agnostic entities representing mathematical or CS objects")
    transitions: List[Dict[str, Any]] = Field(default_factory=list, description="State machine transitions describing pure conceptual behavior (e.g., bundling overflow)")

class ConceptArtSpecification30(BaseModel):
    style: StyleParadigmEnum = Field(description="The aesthetic style chosen for the current concept")
    palette: Dict[str, str] = Field(description="Color palette (e.g., hex codes)")
    geometry_rules: Dict[str, Any] = Field(description="Rules for stroke weight, corner radii, etc.")
    ambient_motion: str = Field(description="Description or parameters of continuous background micro-motion")

class DialecticalSceneManifest(BaseModel):
    concept_id: str
    elements: List[Dict[str, Any]] = Field(description="List of all elements and animation calls in the scene")

    # Every element must have a role explicitly assigned
    def validate_roles(self):
        for el in self.elements:
            role = el.get("role")
            if role not in ["ROLE_70_PEDAGOGICAL_TRANSFER", "ROLE_30_SENSORY_CONCEPT_ART"]:
                raise ValueError(f"Element {el.get('id', 'unknown')} has invalid or missing role: {role}")
