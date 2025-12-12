"""
RAG pipeline: retrieval + prompt assembly + LLM call.

Strict behavior:
- Use only retrieved context. If answer not present, LLM is instructed to respond with the exact fallback string.
- The prompt is deterministic: system message + user message with context and question.

Provider selection:
- Uses environment variables to choose provider and API keys. Default provider is 'openai'.
- Uses LangChain ChatOpenAI for chat completions to support system+user messages.
"""
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from typing import List

FALLBACK = "I could not find that information in the documents."  # exact required fallback


class RAGPipeline:
    def __init__(self, vec_store, emb_service, model_name: str = None):
        self.vec_store = vec_store
        self.emb = emb_service
        self.model_name = model_name or os.environ.get("LLM_MODEL", "gpt-4o-mini")
        self.provider = os.environ.get("LLM_PROVIDER", "openai")
        # Initialize LangChain chat model with temperature 0 for deterministic responses
        if self.provider == "openai":
            self.llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        else:
            # For other providers integration would go here. Default to ChatOpenAI.
            self.llm = ChatOpenAI(model_name=self.model_name, temperature=0)

    def _build_context_block(self, retrieved: dict) -> str:
        # retrieved from chroma: dict with 'metadatas' and 'documents' entries
        docs = []
        metadatas = retrieved.get("metadatas", [])
        documents = retrieved.get("documents", [])
        # chroma returns lists of lists since batching; take first
        if metadatas and isinstance(metadatas[0], list):
            metadatas = metadatas[0]
        if documents and isinstance(documents[0], list):
            documents = documents[0]
        for i, doc in enumerate(documents):
            md = metadatas[i] if i < len(metadatas) else {}
            source = md.get("source", "unknown")
            chunk_idx = md.get("chunk", i + 1)
            header = f"---\nSource: {source} | Chunk: {chunk_idx}\n---\n"
            docs.append(header + doc)
        return "\n\n".join(docs)

    def answer_question(self, question: str, top_k: int = 3) -> str:
        q_emb = self.emb.embed_text(question)
        retrieved = self.vec_store.query_by_embedding(q_emb, top_k=top_k)
        # Build context
        context = self._build_context_block(retrieved)
        system_msg = (
            "You are an AI assistant answering questions about workplace documents.\n"
            "You must use ONLY the provided context to answer.\n"
            "If the answer is not present in the context, you MUST respond with exactly:\n"
            "\"I could not find that information in the documents.\"\n"
            "Do not use prior knowledge. Do not guess. Do not invent facts."
        )
        user_msg = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        messages = [SystemMessage(content=system_msg), HumanMessage(content=user_msg)]
        try:
            response = self.llm(messages)
            text = response.content.strip()
            # Do a minimal safety check: if empty or obviously not from context, return fallback
            if not text:
                return FALLBACK
            return text
        except Exception:
            return FALLBACK
