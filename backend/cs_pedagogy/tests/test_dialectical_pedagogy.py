import pytest
from backend.cs_pedagogy.pedagogical_mechanics_70 import PedagogicalMechanics70Engine
from backend.cs_pedagogy.concept_art_director_30 import ConceptArtDirector30
from backend.cs_pedagogy.opposites_integrator import OppositesIntegrator

def test_70_30_separation():
    engine_70 = PedagogicalMechanics70Engine()
    # Ensure 70% engine returns pure mechanics without style colors
    graph = engine_70.generate_base_n_bundling(10, 15)

    # Assert there is no styling attribute in any entity
    for entity in graph.entities:
        assert "color" not in entity
        assert "geometry" not in entity
        assert entity["role"] == "ROLE_70_PEDAGOGICAL_TRANSFER"

def test_style_rotation_non_repeating():
    director_30 = ConceptArtDirector30()
    style_1 = director_30.generate_style_specification().style
    style_2 = director_30.generate_style_specification().style
    style_3 = director_30.generate_style_specification().style

    # Assert consecutive styles are not the same
    assert style_1 != style_2
    assert style_2 != style_3

def test_audit_manifest_validation():
    engine_70 = PedagogicalMechanics70Engine()
    director_30 = ConceptArtDirector30()
    integrator = OppositesIntegrator()

    graph = engine_70.generate_base_n_bundling(10, 15)
    style = director_30.generate_style_specification()

    manifest = integrator.synthesize(graph, style)

    # Perform audit
    audit_results = integrator.audit_manifest(manifest)

    assert audit_results["70_percent"] > 0
    assert audit_results["30_percent"] > 0

    # Check that all items have appropriate roles and none is missing.
    # The synthesize function automatically calls `validate_roles()` which would raise an exception if a role was missing/invalid.
    for el in manifest.elements:
        assert el["role"] in ["ROLE_70_PEDAGOGICAL_TRANSFER", "ROLE_30_SENSORY_CONCEPT_ART"]
