from docx import Document

from app.processors.base import DocumentProcessor, ExtractionResult


class DOCXProcessor(DocumentProcessor):

    def extract_text(self, file_path: str) -> ExtractionResult:

        document = Document(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return ExtractionResult(
            text=text, 
            page_count=None,
            char_count=len(text),
        ) 