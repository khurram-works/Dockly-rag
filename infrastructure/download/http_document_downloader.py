from pathlib import Path
from tempfile import NamedTemporaryFile

import requests

from core.exception import DocumentDownloadError



class HttpDocumentDownloader:
    def download(
        self,
        file_url: str,
        filename: str,
    ) -> tuple[Path, int]: 
        
        extension = Path(filename).suffix
        
        try:
            response = requests.get(
                file_url,
                stream=True,
                timeout=60,
            )
            response.raise_for_status()

            file_size = 0
            with NamedTemporaryFile(
                delete=False,
                suffix=extension,
            ) as temporary_file:
                for chunk in response.iter_content(
                    chunk_size=1024 * 1024,
                ):
                    if chunk:
                        temporary_file.write(chunk)
                        file_size += len(chunk)

                return Path(temporary_file.name), file_size

        except requests.RequestException as error:
            raise DocumentDownloadError(
                f"Failed to download document: {filename}"
            ) from error