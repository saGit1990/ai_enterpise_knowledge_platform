from app.processors.base import DocumentProcessor
from app.processors.docx_processor import DOCXProcessor
from app.processors.pdf_processor import PDFProcessor
from app.processors.txt_processor import TXTProcessor


class ProcessorFactory:

    @staticmethod
    def get_processor(file_type: str) -> DocumentProcessor:

        processors = {
            "pdf": PDFProcessor(),
            "docx": DOCXProcessor(),
            "txt": TXTProcessor(),
        }

        processor = processors.get(file_type.lower())

        if processor is None:
            raise ValueError(f"Unsupported file type: {file_type}")

        return processor