from abc import ABC, abstractmethod
from dataclasses import dataclass

from fastapi import UploadFile


@dataclass
class StorageResult:
    original_filename: str
    stored_filename: str
    storage_path: str
    file_size: int
    mime_type: str | None


class StorageService(ABC):

    @abstractmethod
    async def save(self, file: UploadFile) -> StorageResult:
        pass

    @abstractmethod
    async def delete(self, storage_path: str) -> None:
        pass

    @abstractmethod
    def exists(self, storage_path: str) -> bool:
        pass