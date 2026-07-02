from uuid import UUID

from app.models.document_content import DocumentContent
from app.processors.base import ExtractionResult
from app.repositories.document_content_repository import (
    DocumentContentRepository,
)


class DocumentContentService:

    def __init__(
        self,
        repository: DocumentContentRepository,
    ):
        self.repository = repository

    async def create_content(
        self,
        document_id: UUID,
        extraction_result: ExtractionResult,
    ) -> DocumentContent:

        return await self.repository.create(
            document_id=document_id,
            raw_text=extraction_result.text,
            page_count=extraction_result.page_count,
            char_count=extraction_result.char_count,
        )

    async def get_content(
        self,
        document_id: UUID,
    ) -> DocumentContent | None:

        return await self.repository.get_by_document_id(document_id)