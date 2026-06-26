from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService
from fastapi import APIRouter, Depends, File, UploadFile
from app.storage.local_storage import LocalStorageService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse)
async def create_document(
    document: DocumentCreate,
    session: AsyncSession = Depends(get_db_session),
):
    repository = DocumentRepository(session)
    service = DocumentService(repository)

    return await service.create_document(document)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session),
):
    repository = DocumentRepository(session)
    storage_service = LocalStorageService()
    service = DocumentService(repository, storage_service)

    return await service.upload_document(file) 