from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class PipelineState(BaseModel):
    job_id: str = Field(..., description="Unique identifier for the pipeline job")
    status: str = Field("initialized", description="Current status of the pipeline")
    checkpoints: List[str] = Field(default_factory=list, description="List of completed checkpoints")

    # Adult-ADHD optimized pedagogical state
    active_concept_art_paradigm: str = Field(default="cyberpunk", description="Active 30% Concept-Art paradigm")
    pedagogical_state: str = Field(default="70%_isomorphic", description="70% Pedagogical state")
    interaction_triggers: List[str] = Field(default_factory=list, description="90/10 interaction triggers")

    # Internal pipeline data
    ingested_data: Optional[Dict[str, Any]] = None
    synthesized_pedagogy: Optional[Dict[str, Any]] = None
    tts_manifest: Optional[Dict[str, Any]] = None
    render_manifest: Optional[Dict[str, Any]] = None

    def mark_checkpoint(self, checkpoint: str):
        self.checkpoints.append(checkpoint)

    def update_status(self, new_status: str):
        self.status = new_status
