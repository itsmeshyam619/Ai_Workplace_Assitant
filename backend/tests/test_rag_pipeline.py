import pytest
from backend.services.rag_pipeline import RAGPipeline, FALLBACK


class DummyVecStore:
    def query_by_embedding(self, embedding, top_k=3):
        # return empty retrieval structure
        return {"metadatas": [[]], "documents": [[]], "distances": [[]]}


class DummyEmb:
    def embed_text(self, text):
        return [0.0] * 384


class DummyLLM:
    def __call__(self, messages):
        class Resp:
            def __init__(self):
                self.content = "I could not find that information in the documents."
        return Resp()


def test_rag_fallback(monkeypatch):
    vec = DummyVecStore()
    emb = DummyEmb()
    pipeline = RAGPipeline(vec_store=vec, emb_service=emb)
    # patch pipeline.llm to deterministic dummy
    pipeline.llm = DummyLLM()
    ans = pipeline.answer_question("Who owns the company?")
    assert ans == FALLBACK
