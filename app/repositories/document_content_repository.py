from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document_content import DocumentContent

from uuid import UUID

class DocumentContentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        document_id,
        raw_text,
        page_count,
        char_count,
    ) -> DocumentContent:

        content = DocumentContent(
            document_id=document_id,
            raw_text=raw_text,
            page_count=page_count,
            char_count=char_count,
        )

        self.session.add(content)

        await self.session.commit()

        await self.session.refresh(content)

        return content
    
    async def get_by_document_id(
        self,
        document_id: UUID,
    ) -> DocumentContent | None:

        stmt = select(DocumentContent).where(
            DocumentContent.document_id == document_id
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()