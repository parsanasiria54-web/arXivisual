import pytest
from backend.core_ingestion.interfaces import AtomicConceptNode, ConceptDependencyDAG, IngestionSource, SourceType
from backend.core_ingestion.cognitive_decomposer import CognitiveDecomposer, CycleDetectedException
from backend.core_ingestion.extractors.arxiv_extractor import ArxivExtractor
from backend.core_ingestion.extractors.document_and_topic_extractor import DocumentAndTopicExtractor

def test_topological_bottom_up_ordering():
    decomposer = CognitiveDecomposer()

    nodes = {
        "A": AtomicConceptNode(id="A", name="A", description="A", prerequisites=[]),
        "B": AtomicConceptNode(id="B", name="B", description="B", prerequisites=["A"]),
        "C": AtomicConceptNode(id="C", name="C", description="C", prerequisites=["B"])
    }

    dag = ConceptDependencyDAG(nodes=nodes, root_id="C")
    order = decomposer.topological_sort(dag)

    assert order == ["A", "B", "C"]
    assert dag.nodes["A"].level == 0
    assert dag.nodes["B"].level == 1
    assert dag.nodes["C"].level == 2

def test_cycle_detection():
    decomposer = CognitiveDecomposer()

    nodes = {
        "A": AtomicConceptNode(id="A", name="A", description="A", prerequisites=["C"]),
        "B": AtomicConceptNode(id="B", name="B", description="B", prerequisites=["A"]),
        "C": AtomicConceptNode(id="C", name="C", description="C", prerequisites=["B"])
    }

    dag = ConceptDependencyDAG(nodes=nodes, root_id="C")

    with pytest.raises(CycleDetectedException):
        decomposer.topological_sort(dag)

def test_working_memory_refresher_injection():
    decomposer = CognitiveDecomposer()

    nodes = {
        "A": AtomicConceptNode(id="A", name="A", description="A", prerequisites=[]),
        "B": AtomicConceptNode(id="B", name="B", description="B", prerequisites=["A"]),
        "C": AtomicConceptNode(id="C", name="C", description="C", prerequisites=["B"]),
        "D": AtomicConceptNode(id="D", name="D", description="D", prerequisites=["C", "A"]) # A is > 2 scenes old
    }

    dag = ConceptDependencyDAG(nodes=nodes, root_id="D")

    scene_timeline = ["A", "B", "C"]
    anchors = decomposer.calculate_working_memory_anchors(scene_timeline, 3, dag, "D")

    assert len(anchors) == 1
    assert anchors[0].concept_id == "A"

def test_multi_source_extraction():
    arxiv_ext = ArxivExtractor()
    doc_ext = DocumentAndTopicExtractor()

    arxiv_source = IngestionSource(source_type=SourceType.ARXIV, content="https://arxiv.org/abs/1706.03762")
    res = arxiv_ext.extract(arxiv_source)
    assert "1706.03762" in res

    topic_source = IngestionSource(source_type=SourceType.TOPIC, content="TCP")
    res = doc_ext.extract(topic_source)
    assert "TCP" in res

    pdf_source = IngestionSource(source_type=SourceType.PDF, content="test.pdf", language="fa")
    res = doc_ext.extract(pdf_source)
    assert "Persian/English text extraction" in res
