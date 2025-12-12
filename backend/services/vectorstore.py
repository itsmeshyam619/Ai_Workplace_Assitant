"""
Vector store service wrapping local ChromaDB.
Persists to the provided directory and provides upsert/query helpers.
"""
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings


class VectorStore:
    def __init__(self, persist_directory: str, embedding_fn):
        """
        persist_directory: path where ChromaDB will store data
        embedding_fn: function(list[str]) -> list[list[float]] used if needed externally
        """
        self.persist_directory = persist_directory
        # Initialize chroma client with local persistence (duckdb+parquet)
        self.client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_directory))
        self.collection = self.client.get_or_create_collection(name="documents")
        self.embedding_fn = embedding_fn

    def upsert(self, ids: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], documents: List[str]):
        # Add/replace vectors in the collection
        self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

    def query_by_embedding(self, embedding: List[float], top_k: int = 3):
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k, include=["metadatas", "documents", "distances"]) 
        # results is a dict with lists
        return results

    def persist(self):
        try:
            self.client.persist()
        except Exception:
            pass
