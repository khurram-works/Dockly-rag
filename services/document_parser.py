import requests
import tempfile
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from unstructured.partition.auto import partition
from pathlib import Path
from services.text_cleaner import normalize_text
from services.element_filter import filter_elements

def download_and_parse_document(file_url: str, filename: str) -> tuple[list[dict], int]:
    # Download file

    # Save temporary file

    # Parse with Unstructured

    # Normalize into our format

    # Return pages
    response = requests.get(file_url, timeout=30)
    response.raise_for_status()
    extension = Path(filename).suffix.lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
        tmp_file.write(response.content)
        tmp_path = tmp_file.name


    try:
        elements = partition(
            filename=tmp_path,
            strategy="hi_res" if extension in [".pdf", ".png", ".jpg"] else "fast"
            )
        
        document_elements=[]
        for element in elements:
            # print("=" * 60)
            # print(type(element).__name__)
            # print(element.text)
            # print(element.metadata)
            element_type = type(element).__name__
            text = normalize_text(element.text)
            # print(text)
            if not text:
                continue
            page_number = getattr(
                element.metadata,
                "page_number",
                None
            ) or 1

            document_element = {
                "text": text,
                "pageNumber": page_number,
                "elementType": element_type,
                "metadata": {
                    "pageNumber": page_number,
                },
            }
            document_elements.append(document_element)
        
        if document_elements:
            page_count = max(
                page["pageNumber"]
                for element in document_elements
            )
        else:
            page_count = 1
        filtered_elements = filter_elements(document_elements)
        return filtered_elements, page_count
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def split_text_into_chunks(elements: list[dict]) ->list[dict]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )

    all_chunks = []

    for element in elements:
        element_chunks = splitter.split_text(element["text"])

        for chunk in element_chunks:
            if len(chunk.strip()) > 50:
                all_chunks.append({
                    "text": chunk,
                    "pageNumber": element["pageNumber"],
                    "elementType": element["elementType"],
                    "metadata": element["metadata"]
                })
    print(f"Created {len(all_chunks)} chunks")

    return all_chunks










    





