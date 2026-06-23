from sqlalchemy.ext.asyncio import AsyncSession

from app.models.documents import Document


class DocumentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(
        self,
        filename: str,
        file_type: str,
    ) -> Document:

        document = Document(
            filename=filename,
            file_type=file_type,
        )

        self.session.add(document)

        await self.session.commit()

        await self.session.refresh(document)

        return document