import re

def normalize_text(text: str)->str:
  """
    Normalize extracted text before chunking.
  """
  # Remove leading/trailing whitespace
  text = text.strip()
  # Replace tabs with spaces
  text = text.replace("\t", " ")
  # Replace multiple spaces with one
  text = re.sub(r"[ ]+", " ", text)
  # Replace 3 or more newlines with 2
  text = re.sub(r"\n{3,}", "\n\n", text)

  return text
