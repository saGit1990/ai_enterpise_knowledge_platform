from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ExtractionResult:
    text: str
    page_count: int | None
    char_count: int


class DocumentProcessor(ABC):

    @abstractmethod
    def extract_text(self, file_path: str) -> ExtractionResult:
        pass