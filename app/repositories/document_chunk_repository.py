from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.chunking.base import TextChunk
from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(
        self,
        document_id: UUID,
        document_content_id: UUID,
        chunks: list[TextChunk],
    ) -> list[DocumentChunk]:
        document_chunks = [
            DocumentChunk(
                document_id=document_id,
                document_content_id=document_content_id,
                chunk_index=chunk.chunk_index,
                chunk_text=chunk.text,
                start_char=chunk.start_char,
                end_char=chunk.end_char,
                char_count=chunk.char_count,
                token_estimate=chunk.token_estimate,
            )
            for chunk in chunks
        ]

        self.session.add_all(document_chunks)
        await self.session.commit()

        for chunk in document_chunks:
            await self.session.refresh(chunk)

        return document_chunks

    async def get_by_document_id(
        self,
        document_id: UUID,
    ) -> list[DocumentChunk]:
        stmt = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def delete_by_document_id(
        self,
        document_id: UUID,
    ) -> None:
        stmt = delete(DocumentChunk).where(
            DocumentChunk.document_id == document_id
        )

        await self.session.execute(stmt)
        await self.session.commit()