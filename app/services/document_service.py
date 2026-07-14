from fastapi import UploadFile

from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate
from app.services.document_content_service import DocumentContentService
from app.services.extraction_service import ExtractionService
from app.storage.base import StorageService


class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
        storage_service: StorageService | None = None,
        extraction_service: ExtractionService | None = None,
        document_content_service: DocumentContentService | None = None,
    ):
        self.repository = repository
        self.storage_service = storage_service
        self.extraction_service = extraction_service
        self.document_content_service = document_content_service

    async def create_document(self, document: DocumentCreate):
        return await self.repository.create_document(
            filename=document.filename,
            file_type=document.file_type,
            storage_path=document.storage_path,
            file_size=document.file_size,
            mime_type=document.mime_type,
            processing_status=document.processing_status,
        )

    async def upload_document(self, file: UploadFile):
        if self.storage_service is None:
            raise ValueError("Storage service is required for file upload")

        if self.extraction_service is None:
            raise ValueError("Extraction service is required for file upload")

        if self.document_content_service is None:
            raise ValueError("Document content service is required for file upload")

        storage_result = await self.storage_service.save(file)

        file_type = storage_result.original_filename.split(".")[-1].lower()

        document = await self.repository.create_document(
            filename=storage_result.original_filename,
            file_type=file_type,
            storage_path=storage_result.storage_path,
            file_size=storage_result.file_size,
            mime_type=storage_result.mime_type,
            processing_status="uploaded",
        )

        extraction_result = self.extraction_service.extract(
            file_path=storage_result.storage_path,
            file_type=file_type,
        )

        await self.document_content_service.create_content(
            document_id=document.id,
            extraction_result=extraction_result,
        )

        updated_document = await self.repository.update_processing_status(
            document_id=document.id,
            processing_status="extracted",
        )

        return updated_document