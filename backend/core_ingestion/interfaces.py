from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from enum import Enum

class SourceType(str, Enum):
    ARXIV = "arxiv"
    TOPIC = "topic"
    MARKDOWN = "markdown"
    PDF = "pdf"

class IngestionSource(BaseModel):
    source_type: SourceType = Field(..., description="The type of the ingestion source")
    content: str = Field(..., description="The main content or identifier (e.g., topic string, arxiv ID, raw text)")
    language: str = Field("en", description="Language preference (e.g., 'en', 'fa')")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata for the source")

class AtomicConceptNode(BaseModel):
    id: str = Field(..., description="Unique identifier for the concept")
    name: str = Field(..., description="Name of the atomic concept")
    description: str = Field(..., description="Detailed description or definition of the concept")
    level: int = Field(0, description="Topological level: 0 for axioms/leaves, higher for complex concepts")
    prerequisites: List[str] = Field(default_factory=list, description="List of prerequisite concept IDs")

class ConceptDependencyDAG(BaseModel):
    nodes: Dict[str, AtomicConceptNode] = Field(default_factory=dict, description="Dictionary mapping concept IDs to AtomicConceptNode objects")
    root_id: Optional[str] = Field(None, description="The ID of the root/holistic concept for this DAG")

class AVStimulusDirective(BaseModel):
    visual_pacing: str = Field(..., description="Pacing description (e.g., fast, dynamic, focused)")
    color_contrast_cue: str = Field(..., description="Color and contrast cues for visual engagement")
    motion_metaphor: str = Field(..., description="Metaphorical motion to describe the concept visually")
    audio_tone_shift: str = Field(..., description="Tone shift in audio to keep attention")

class WorkingMemoryAnchor(BaseModel):
    concept_id: str = Field(..., description="The ID of the concept to be anchored")
    visual_reminder: str = Field(..., description="A short visual reminder or icon description for the screen")

class MicroSceneScript(BaseModel):
    scene_id: str = Field(..., description="Unique identifier for the scene")
    duration_seconds: int = Field(..., ge=15, le=35, description="Duration of the scene in seconds (15-35s)")
    narrative_text: str = Field(..., description="The narrative exposition for this micro-scene")
    av_stimulus: AVStimulusDirective = Field(..., description="Audio-visual stimulus directives for engagement")
    working_memory_anchors: List[WorkingMemoryAnchor] = Field(default_factory=list, description="Working memory anchors to offload cognitive strain for concepts >2 scenes old")
    primary_concept_id: str = Field(..., description="The main concept ID being taught in this scene")
