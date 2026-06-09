# import fitz          # fitz is the import name for PyMuPDF
# import requests      # for downloading the PDF from Supabase URL
# import tempfile      # for creating a temporary file on disk
# import os
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # ─────────────────────────────────────────────
# # download_and_extract_text
# # Takes a Supabase URL, downloads the PDF,
# # extracts all text, returns the text as a string
# # ─────────────────────────────────────────────
# def download_and_extract_text(file_url: str) -> tuple[str, int]:
#     # tuple[str, int] means this function returns TWO things:
#     # 1. The extracted text (string)
#     # 2. The number of pages (integer)

#     # Step 1: Download the PDF from Supabase
#     # requests.get() is like fetch() in JavaScript
#     # It makes an HTTP GET request to the URL and returns the response
#     response = requests.get(file_url)

#     # Check if download succeeded
#     # status_code 200 means success, anything else means failure
#     if response.status_code != 200:
#         raise Exception(f"Failed to download PDF: {response.status_code}")
#     # raise Exception is like throw new Error() in JavaScript
#     # The f"..." is an f-string — like template literals in JavaScript
#     # f"Hello {name}" is the same as `Hello ${name}` in JavaScript

#     # Step 2: Save the downloaded PDF to a temporary file
#     # Why a temporary file? PyMuPDF needs to open a file from disk
#     # It cannot read directly from memory bytes
#     # tempfile.NamedTemporaryFile creates a file that auto-deletes when done
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#         tmp_file.write(response.content)
#         # response.content = the raw bytes of the PDF
#         tmp_path = tmp_file.name
#         # tmp_path = something like "/tmp/abc123.pdf"

#     # Step 3: Open the PDF with PyMuPDF and extract text
#     try:
#         pdf_document = fitz.open(tmp_path)
#         # fitz.open() opens the PDF file — like opening a book

#         page_count = len(pdf_document)
#         # len() on a PDF gives you the number of pages

#         full_text = ""
#         # We'll build up the complete text here

#         for page_number in range(page_count):
#             # range(page_count) = [0, 1, 2, 3, ...] one number per page
#             page = pdf_document[page_number]
#             # Get the page object at this index

#             page_text = page.get_text()
#             # get_text() extracts all the text from this page as a string

#             full_text += f"\n[Page {page_number + 1}]\n{page_text}"
#             # We add a page marker before each page's text
#             # This helps us track which page each chunk came from
#             # page_number + 1 because pages start at 0 but humans count from 1

#         pdf_document.close()
#         # Always close the document when done — frees memory

#         return full_text, page_count
#         # Return both values — the caller gets both

#     finally:
#         # finally runs whether the try succeeded or failed
#         # We always want to delete the temporary file
#         os.unlink(tmp_path)
#         # os.unlink() deletes a file — like rm in terminal


# # ─────────────────────────────────────────────
# # split_text_into_chunks
# # Takes a big string of text and splits it into
# # smaller overlapping pieces ready for embedding
# # ─────────────────────────────────────────────
# def split_text_into_chunks(text: str) -> list[str]:

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         # Each chunk will be at most 1000 characters
#         # 1000 characters ≈ about 150-200 words

#         chunk_overlap=200,
#         # The last 200 characters of each chunk are repeated
#         # at the start of the next chunk
#         # This prevents losing context at chunk boundaries

#         length_function=len,
#         # How to measure length — just count characters

#         separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
#         # Try to split at these boundaries in order:
#         # First try double newline (paragraph break)
#         # Then single newline
#         # Then sentence endings
#         # Then commas
#         # Then spaces (word boundary)
#         # Last resort: split anywhere
#         # This makes chunks split at natural language boundaries
#     )

#     chunks = splitter.split_text(text)
#     # split_text() returns a list of strings
#     # Each string is one chunk

#     # Filter out chunks that are too short to be meaningful
#     # A chunk with only 50 characters is probably a page header or whitespace
#     chunks = [chunk for chunk in chunks if len(chunk.strip()) > 50]
#     # This is a list comprehension — like array.filter() in JavaScript
#     # chunk.strip() removes whitespace from start and end
#     # We keep only chunks longer than 50 characters

#     return chunks

import fitz
import requests
import tempfile
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def download_and_extract_text(file_url: str) -> tuple[str, int]:
    file = requests.get(file_url)
    
    if file.status_code != 200:
        raise Exception(f"Failed to download the PDF: {file.status_code}")
    

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file.content)
        tmp_path = tmp_file.name


    try:
        pdf_document = fitz.open(tmp_path)
        page_count = len(pdf_document)

        full_text = ""

        for page_number in range(page_count):
            page = pdf_document[page_count]
            page_text = page.get_text()
            full_text += f"\n[Page {page_number + 1}]\n{page_text}"

        pdf_document.close()

        return full_text, page_count
    finally:
        os.unlink(tmp_path)

def split_text_into_chunks(text: str) ->list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )

    chunks = splitter.split_text(text)

    chunks = [chunk for chunk in chunks if len(chunk.strip())>50]

    return chunks










    





