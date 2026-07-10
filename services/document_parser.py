import fitz
import requests
import tempfile
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from unstructured.partition.auto import partition
from pathlib import Path

def download_and_parse_document(file_url: str, filename: str) -> tuple[list[dict], int]:
    response = requests.get(file_url, timeout=30)
    response.raise_for_status()
    extension = Path(filename).suffix.lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
        tmp_file.write(response.content)
        tmp_path = tmp_file.name


    try:
        # with fitz.open(tmp_path) as pdf_document:
        #     page_count = len(pdf_document)
    
        #     pages= []
        #     for page_number in range(page_count):
        #         page = pdf_document[page_number]
        #         page_text = page.get_text()
        #         if page_text.strip():
        #             pages.append({
        #                 "text": page_text,
        #                 "pageNumber": page_number + 1
        #             })
        #         print(f"Extracted {len(pages)} pages")
        # return pages, page_count
        elements = partition(filename=tmp_path)
        pages=[]
        for element in elements:
            text=element.text
            if not text or not text.strip():
                continue
            page_number = getattr(
               element.metadata,
               "page_number",
               1,
            )
            pages.append({
                "text": text,
                "pageNumber": page_number
            })
        
        if pages:
            page_count = max(
                page["pageNumber"]
                for page in pages
            )
        else:
            page_count = 1
        return pages, page_count
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def split_text_into_chunks(pages: list[dict]) ->list[dict]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )

    all_chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk in page_chunks:
            if len(chunk.strip()) > 50:
                all_chunks.append({
                    "text": chunk,
                    "pageNumber": page["pageNumber"]
                })

    print(f"Created {len(all_chunks)} chunks")

    return all_chunks










    





