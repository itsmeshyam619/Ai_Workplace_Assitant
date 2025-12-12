"""
Embedding service using sentence-transformers/all-MiniLM-L6-v2.
This wraps the model to provide a simple function for embedding lists of texts.
"""
from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load once on initialization. This may be slow on first import.
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        # Keep batching implicit; the library handles it.
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_text(self, text: str) -> List[float]:
        return self.embed_texts([text])[0]
