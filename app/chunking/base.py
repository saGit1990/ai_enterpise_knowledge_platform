from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TextChunk:
    chunk_index: int
    text: str
    start_char: int
    end_char: int
    char_count: int
    token_estimate: int


class ChunkingStrategy(ABC):

    @abstractmethod
    def chunk(self, text: str) -> list[TextChunk]:
        pass