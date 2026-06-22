import os
from typing import List
import openai

class EmbeddingClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.model = "text-embedding-3-small"
        self.embedding_dim = 1536

    def embed_text(self, text: str) -> List[float]:
        response = openai.Embedding.create(
            input=text,
            model=self.model,
            api_key=self.api_key
        )
        embedding = response['data'][0]['embedding']
        if len(embedding) != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch: expected {self.embedding_dim}, got {len(embedding)}")
        return embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = openai.Embedding.create(
            input=texts,
            model=self.model,
            api_key=self.api_key
        )
        embeddings = [item['embedding'] for item in response['data']]
        for embedding in embeddings:
            if len(embedding) != self.embedding_dim:
                raise ValueError(f"Embedding dimension mismatch: expected {self.embedding_dim}, got {len(embedding)}")
        return embeddings

def get_embedding(texts: List[str]) -> List[List[float]]:
    client = EmbeddingClient()
    return client.embed_batch(texts)