import fitz
import requests
import tempfile
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def download_and_extract_text(file_url: str) -> tuple[list[dict], int]:
    response = requests.get(file_url, timeout=30)
    response.raise_for_status()
    

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(response.content)
        tmp_path = tmp_file.name


    try:
        with fitz.open(tmp_path) as pdf_document:
            page_count = len(pdf_document)
    
            pages= []
            for page_number in range(page_count):
                page = pdf_document[page_number]
                page_text = page.get_text()
                if page_text.strip():
                    pages.append({
                        "text": page_text,
                        "pageNumber": page_number + 1
                    })
                print(f"Extracted {len(pages)} pages")
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










    





