import fitz

from app.processors.base import DocumentProcessor, ExtractionResult


class PDFProcessor(DocumentProcessor):

    def extract_text(self, file_path: str) -> ExtractionResult:
        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        return ExtractionResult(
            text=text,
            page_count=len(document),
            char_count=len(text),
        )