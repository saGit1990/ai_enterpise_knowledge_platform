from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate
from fastapi import UploadFile, HTTPException
from app.storage.base import StorageService

class DocumentService:

    def __init__(self, repository: DocumentRepository, 
        storage_service: StorageService | None = None):
        self.repository = repository
        self.storage_service = storage_service
        self.allowed_extensions = ['pdf','docx','txt','csv']

    async def create_document(
        self,
        document: DocumentCreate,
    ):
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
        
        if file.size == 0:
            raise HTTPException(
                status_code=400,
                detail="Please upload the file"
            )
                
        extensions = file.filename.split('.')[-1].lower()
        print(f'The extnsion is {extensions}')

        if extensions not in self.allowed_extensions:
            raise HTTPException(
                status_code=415,
                detail="Unsuppoerted file type. Only allowed extensions are pdf, txt, docx, csv"
            )

        storage_result = await self.storage_service.save(file)

        file_type = storage_result.original_filename.split(".")[-1].lower()

        return await self.repository.create_document(
            filename=storage_result.original_filename,
            file_type=file_type,
            storage_path=storage_result.storage_path,
            file_size=storage_result.file_size,
            mime_type=storage_result.mime_type,
            processing_status="uploaded",
        )
    