from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Dict, Any

from backend.core_ingestion.interfaces import IngestionSource, SourceType
from backend.core_ingestion.extractors.arxiv_extractor import ArxivExtractor
from backend.core_ingestion.extractors.document_and_topic_extractor import DocumentAndTopicExtractor
from backend.core_ingestion.cognitive_decomposer import CognitiveDecomposer
from backend.core_ingestion.narrative_weaver import NarrativeWeaver

router = APIRouter(prefix="/api/v1/ingestion", tags=["ingestion"])

class TopicRequest(BaseModel):
    content: str
    language: str = "en"
    source_type: SourceType = SourceType.TOPIC

@router.post("/decompose-topic")
async def decompose_topic(request: TopicRequest):
    source = IngestionSource(
        source_type=request.source_type,
        content=request.content,
        language=request.language
    )

    # Process extraction
    if request.source_type == SourceType.ARXIV:
        extractor = ArxivExtractor()
    else:
        extractor = DocumentAndTopicExtractor()

    extracted_text = extractor.extract(source)

    # Process decomposition and weaving
    decomposer = CognitiveDecomposer()
    dag = decomposer.decompose(extracted_text)

    weaver = NarrativeWeaver(decomposer)
    scenes = weaver.weave(dag)

    return {
        "dag": dag.model_dump(),
        "scenes": [s.model_dump() for s in scenes]
    }

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...), language: str = Form("en")):
    # Mocking reading the file content
    content = file.filename
    source_type = SourceType.PDF if content.endswith(".pdf") else SourceType.MARKDOWN

    source = IngestionSource(
        source_type=source_type,
        content=content,
        language=language
    )

    extractor = DocumentAndTopicExtractor()
    extracted_text = extractor.extract(source)

    decomposer = CognitiveDecomposer()
    dag = decomposer.decompose(extracted_text)

    weaver = NarrativeWeaver(decomposer)
    scenes = weaver.weave(dag)

    return {
        "dag": dag.model_dump(),
        "scenes": [s.model_dump() for s in scenes]
    }
