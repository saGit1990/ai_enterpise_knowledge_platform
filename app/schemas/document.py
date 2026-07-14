from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    filename: str
    file_type: str
    storage_path: str | None = None
    file_size: int | None = None
    mime_type: str | None = None
    processing_status: str = "uploaded"


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_type: str
    storage_path: str | None
    file_size: int | None
    mime_type: str | None
    processing_status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class DocumentChunkResponse(BaseModel):
    id: UUID
    document_id: UUID
    document_content_id: UUID
    chunk_index: int
    chunk_text: str
    start_char: int
    end_char: int
    char_count: int
    token_estimate: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }