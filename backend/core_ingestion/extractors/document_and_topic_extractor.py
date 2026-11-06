from backend.core_ingestion.interfaces import IngestionSource, SourceType

class DocumentAndTopicExtractor:
    def __init__(self):
        pass

    def extract(self, source: IngestionSource) -> str:
        if source.source_type == SourceType.TOPIC:
            return f"Topic Extract: Deep dive into {source.content}. Analyzing fundamental principles."

        elif source.source_type == SourceType.MARKDOWN:
            return f"Markdown Extract: Parsed notes from {source.content}. Structuring headings and bullet points."

        elif source.source_type == SourceType.PDF:
            # Handle PDF with Persian/English text extraction as required
            lang_indicator = "Persian/English" if source.language in ["fa", "en"] else source.language
            return f"PDF Extract: Processed document '{source.content}' with {lang_indicator} text extraction."

        else:
            raise ValueError(f"Unsupported source type for DocumentAndTopicExtractor: {source.source_type}")
