from app.processors.base import ExtractionResult
from app.processors.factory import ProcessorFactory


class ExtractionService:
    def extract(self, file_path: str, file_type: str) -> ExtractionResult:
        processor = ProcessorFactory.get_processor(file_type)
        return processor.extract_text(file_path)