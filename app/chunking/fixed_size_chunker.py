from app.chunking.base import ChunkingStrategy, TextChunk


class FixedSizeChunker(ChunkingStrategy):

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[TextChunk]:
        if not text or not text.strip():
            return []

        chunks: list[TextChunk] = []

        start = 0
        chunk_index = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    TextChunk(
                        chunk_index=chunk_index,
                        text=chunk_text,
                        start_char=start,
                        end_char=end,
                        char_count=len(chunk_text),
                        token_estimate=max(1, len(chunk_text) // 4),
                    )
                )

                chunk_index += 1

            start += self.chunk_size - self.overlap

        return chunks