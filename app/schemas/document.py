from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    filename: str
    file_type: str


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_type: str
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }