from app.processors.base import DocumentProcessor, ExtractionResult


class TXTProcessor(DocumentProcessor):

    def extract_text(self, file_path: str) -> ExtractionResult:

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        return ExtractionResult(
            text=text,
            page_count=None,
            char_count=len(text),
        )