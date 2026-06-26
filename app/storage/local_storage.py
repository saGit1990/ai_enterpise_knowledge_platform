import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.storage.base import StorageResult, StorageService


class LocalStorageService(StorageService):

    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, file: UploadFile) -> StorageResult:
        original_filename = file.filename or "uploaded_file"
        stored_filename = f"{uuid.uuid4()}_{original_filename}"
        storage_path = self.upload_dir / stored_filename

        file.file.seek(0)

        with storage_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = storage_path.stat().st_size

        return StorageResult(
            original_filename=original_filename,
            stored_filename=stored_filename,
            storage_path=str(storage_path),
            file_size=file_size,
            mime_type=file.content_type,
        )

    async def delete(self, storage_path: str) -> None:
        path = Path(storage_path)
        if path.exists():
            path.unlink()

    def exists(self, storage_path: str) -> bool:
        return Path(storage_path).exists()