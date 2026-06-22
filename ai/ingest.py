import os
from typing import List, Dict
from pypdf import PdfReader
from docx import Document
from .embeddings import get_embedding
from .vector_store import VectorStore

def chunk(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def ingest_document(file_path: str, session_id: str, user_id: str) -> Dict[str, int]:
    vector_store = VectorStore()
    file_extension = os.path.splitext(file_path)[1].lower()
    text = ""

    # Extract text based on file type
    if file_extension == ".pdf":
        reader = PdfReader(file_path)
        text = " ".join(page.extract_text() for page in reader.pages)
    elif file_extension == ".docx":
        doc = Document(file_path)
        text = " ".join(paragraph.text for paragraph in doc.paragraphs)
    elif file_extension in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    # Chunk the text
    chunks = chunk(text)

    # Embed and upsert each chunk
    embeddings = get_embedding(chunks)
    for i, embedding in enumerate(embeddings):
        metadata = {
            "session_id": session_id,
            "user_id": user_id,
            "source": file_path,
            "chunk_text": chunks[i],
        }
        vector_store.upsert(id=f"{session_id}_{user_id}_{i}", vector=embedding, metadata=metadata)

    return {"chunks": len(chunks)}