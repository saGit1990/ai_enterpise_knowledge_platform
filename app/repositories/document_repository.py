from sqlalchemy.ext.asyncio import AsyncSession

from app.models.documents import Document


class DocumentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(
        self,
        filename: str,
        file_type: str,
        storage_path: str | None = None,
        file_size: int | None = None,
        mime_type: str | None = None,
        processing_status: str = "uploaded",
    ) -> Document:

        document = Document(
            filename=filename,
            file_type=file_type,
            storage_path=storage_path,
            file_size=file_size,
            mime_type=mime_type,
            processing_status=processing_status,
        )

        self.session.add(document)

        await self.session.commit()

        await self.session.refresh(document)

        return document