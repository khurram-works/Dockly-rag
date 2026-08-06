EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
EMBEDDING_BATCH_SIZE = 32

DEFAULT_MAX_CHARACTERS = 1500
DEFAULT_NEW_AFTER_N_CHARS = 1000
DEFAULT_COMBINE_TEXT_UNDER_N_CHARS = 1000
DEFAULT_DISTANCE = "cosine"
DEFAULT_COLLECTION_NAME = "dockly_documents"
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024
SUPPORTED_FILE_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".html",
    ".txt", ".md", ".csv", ".epub",
    ".jpg", ".jpeg", ".png"
}