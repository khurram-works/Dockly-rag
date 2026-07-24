from abc import ABC, abstractmethod
from pathlib import Path


class FileDownloader(ABC):

    @abstractmethod
    def download(
        self,
        file_url: str,
        filename: str,
    ) -> Path:
        pass