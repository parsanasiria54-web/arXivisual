import pytest
from backend.core_orchestrator.conductor import Conductor
from backend.core_orchestrator.pipeline_state import PipelineState

@pytest.mark.asyncio
async def test_end_to_end_pipeline():
    conductor = Conductor()
    request_data = {"job_id": "test_job_123", "topic": "DSA"}
    state = await conductor.execute_pipeline(request_data)

    assert isinstance(state, PipelineState)
    assert state.job_id == "test_job_123"
    assert state.status == "completed"

    assert "ingestion_complete" in state.checkpoints
    assert "pedagogy_complete" in state.checkpoints
    assert "tts_complete" in state.checkpoints
    assert "render_complete" in state.checkpoints

    assert state.ingested_data is not None
    assert state.synthesized_pedagogy is not None
    assert state.tts_manifest is not None
    assert state.render_manifest is not None
