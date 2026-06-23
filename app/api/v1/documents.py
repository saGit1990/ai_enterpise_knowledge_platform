from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse)
async def create_document(
    document: DocumentCreate,
    session: AsyncSession = Depends(get_db_session),
):
    repository = DocumentRepository(session)
    service = DocumentService(repository)

    return await service.create_document(document)