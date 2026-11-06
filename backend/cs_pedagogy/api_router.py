from fastapi import APIRouter
from backend.cs_pedagogy.pedagogical_mechanics_70 import PedagogicalMechanics70Engine
from backend.cs_pedagogy.concept_art_director_30 import ConceptArtDirector30
from backend.cs_pedagogy.opposites_integrator import OppositesIntegrator
from backend.cs_pedagogy.interfaces import DialecticalSceneManifest

router = APIRouter(prefix="/api/v1/pedagogy", tags=["cs_pedagogy"])

# Initialize engine singletons for the router
engine_70 = PedagogicalMechanics70Engine()
director_30 = ConceptArtDirector30()
integrator = OppositesIntegrator()

@router.get("/generate/base_n_bundling", response_model=DialecticalSceneManifest)
async def generate_base_n_bundling(base: int = 10, units: int = 12):
    """
    Demo endpoint: Generates a Dialectical Scene Manifest for Base-N bundling.
    """
    # 1. 70% pure mechanics
    graph = engine_70.generate_base_n_bundling(base=base, initial_units=units)

    # 2. 30% style rotation
    style = director_30.generate_style_specification()

    # 3. Integration
    manifest = integrator.synthesize(graph, style)

    return manifest

@router.get("/generate/pointer_relinking", response_model=DialecticalSceneManifest)
async def generate_pointer_relinking():
    """
    Demo endpoint: Generates a Dialectical Scene Manifest for pointer relinking.
    """
    graph = engine_70.generate_pointer_relinking("NodeA", "NodeB", "NodeC")
    style = director_30.generate_style_specification()
    manifest = integrator.synthesize(graph, style)
    return manifest
