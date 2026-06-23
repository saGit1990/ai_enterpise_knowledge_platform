from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate


class DocumentService:

    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    async def create_document(
        self,
        document: DocumentCreate,
    ):
        return await self.repository.create_document(
            filename=document.filename,
            file_type=document.file_type,
        )