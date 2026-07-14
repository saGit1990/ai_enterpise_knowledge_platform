from uuid import UUID

from app.chunking.fixed_size_chunker import FixedSizeChunker
from app.models.document_chunk import DocumentChunk
from app.models.document_content import DocumentContent
from app.repositories.document_chunk_repository import DocumentChunkRepository


class ChunkingService:
    def __init__(
        self,
        repository: DocumentChunkRepository,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        self.repository = repository
        self.chunker = FixedSizeChunker(
            chunk_size=chunk_size,
            overlap=overlap,
        )

    async def chunk_document_content(
        self,
        document_id: UUID,
        content: DocumentContent,
    ) -> list[DocumentChunk]:
        chunks = self.chunker.chunk(content.raw_text)

        if not chunks:
            return []

        await self.repository.delete_by_document_id(document_id)

        return await self.repository.create_many(
            document_id=document_id,
            document_content_id=content.id,
            chunks=chunks,
        )