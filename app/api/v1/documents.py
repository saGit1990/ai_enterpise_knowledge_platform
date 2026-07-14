from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.document_content_repository import DocumentContentRepository
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_content_service import DocumentContentService
from app.services.document_service import DocumentService
from app.services.extraction_service import ExtractionService
from app.storage.local_storage import LocalStorageService
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.chunking_service import ChunkingService
from app.schemas.document import DocumentChunkResponse

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
    document_repository = DocumentRepository(session)
    content_repository = DocumentContentRepository(session)

    storage_service = LocalStorageService()
    extraction_service = ExtractionService()
    document_content_service = DocumentContentService(content_repository)

    service = DocumentService(
        repository=document_repository,
        storage_service=storage_service,
        extraction_service=extraction_service,
        document_content_service=document_content_service,
    )

    return await service.upload_document(file)

@router.post(
    "/{document_id}/chunk",
    response_model=list[DocumentChunkResponse],
)
async def chunk_document(
    document_id: UUID,
    session: AsyncSession = Depends(get_db_session),
):
    content_repository = DocumentContentRepository(session)
    chunk_repository = DocumentChunkRepository(session)

    content_service = DocumentContentService(content_repository)
    chunking_service = ChunkingService(chunk_repository)

    content = await content_service.get_content(document_id)

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Extracted content not found for this document.",
        )

    chunks = await chunking_service.chunk_document_content(
        document_id=document_id,
        content=content,
    )

    return chunks