from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from infrastructure.download.http_document_downloader import (
    HttpDocumentDownloader,
)

class TemporaryDocument:
    def __init__(
        self,
        downloader: HttpDocumentDownloader,
    ) -> None:

        self._downloader = downloader

    @contextmanager
    def open(
        self,
        file_url: str,
        filename: str,
    ) -> Iterator[tuple[Path, int]]: 
        file_path, file_size = self._downloader.download(
            file_url=file_url,
            filename=filename,
        )

        try:
            yield file_path, file_size
        finally:
            file_path.unlink(missing_ok=True)