from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from pydantic import BaseModel
from .router_service import RouterService
from .interfaces import LLMRequest, LLMResponse, ModelCapabilities

router = APIRouter(prefix="/api/v1/llm", tags=["LLM Router"])

# In a real app, this would be a dependency injected service
router_service = RouterService()

def get_router_service():
    return router_service

class TestGenerateRequest(BaseModel):
    provider_name: str
    model: str
    prompt: str

@router.get("/providers")
async def get_providers(service: RouterService = Depends(get_router_service)) -> Dict[str, bool]:
    """Returns available local and cloud provider presets and their live health status."""
    return await service.get_health_status()

@router.get("/local-models")
async def get_local_models(service: RouterService = Depends(get_router_service)) -> List[ModelCapabilities]:
    """Queries local Ollama and returns installed models with metadata."""
    if "ollama" not in service.providers:
        raise HTTPException(status_code=404, detail="Ollama provider not configured.")
    return await service.providers["ollama"].list_models()

@router.post("/test-generate")
async def test_generate(req: TestGenerateRequest, service: RouterService = Depends(get_router_service)) -> LLMResponse:
    """Executes a diagnostic prompt on any selected provider/model."""
    llm_req = LLMRequest(
        messages=[{"role": "user", "content": req.prompt}],
        model=req.model,
        temperature=0.0
    )

    try:
        return await service.route_request(req.provider_name, llm_req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
