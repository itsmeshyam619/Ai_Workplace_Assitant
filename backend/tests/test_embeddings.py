from backend.services.embeddings import EmbeddingService


def test_embeddings_shape():
    svc = EmbeddingService()
    texts = ["hello world", "another sentence"]
    embs = svc.embed_texts(texts)
    assert len(embs) == 2
    assert len(embs[0]) > 0
