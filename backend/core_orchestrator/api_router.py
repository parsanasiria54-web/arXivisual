import asyncio
import json
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any

from .conductor import Conductor
from .pipeline_state import PipelineState

router = APIRouter()
conductor = Conductor()

@router.post("/execute", response_model=PipelineState)
async def execute_pipeline_endpoint(request_data: Dict[str, Any]):
    return await conductor.execute_pipeline(request_data)

@router.get("/status/{job_id}", response_model=PipelineState)
async def get_pipeline_status(job_id: str):
    # Dummy mock status
    return PipelineState(job_id=job_id, status="mock_status")

@router.get("/stream/{job_id}")
async def stream_pipeline_status(job_id: str):
    async def event_generator():
        # Mock streaming of status events for the pipeline
        statuses = ["initialized", "ingesting", "synthesizing_pedagogy", "generating_audio", "rendering", "completed"]
        for status in statuses:
            state = PipelineState(job_id=job_id, status=status)
            yield f"data: {state.model_dump_json()}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
