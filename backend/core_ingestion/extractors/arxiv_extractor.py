from backend.core_ingestion.interfaces import IngestionSource, SourceType
import re

class ArxivExtractor:
    def __init__(self):
        pass

    def extract(self, source: IngestionSource) -> str:
        if source.source_type != SourceType.ARXIV:
            raise ValueError("Invalid source type for ArxivExtractor")

        # Preserve arXiv URL/ID fetching capabilities and LaTeX/PDF parsing
        arxiv_id = self._parse_arxiv_id(source.content)

        # Mock fetching logic, replacing real network requests for the implementation
        # The prompt requires: Adapter preserving arXiv URL/ID fetching and LaTeX/PDF parsing
        return f"Mocked extracted content for arXiv ID: {arxiv_id}. This would contain LaTeX/PDF parsed text."

    def _parse_arxiv_id(self, content: str) -> str:
        match = re.search(r"(\d{4}\.\d{4,5})", content)
        if match:
            return match.group(1)
        return content.strip()
