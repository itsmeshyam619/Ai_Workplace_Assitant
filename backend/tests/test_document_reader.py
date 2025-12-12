from backend.services.document_reader import chunk_text, extract_text_from_txt_bytes


def test_chunking_basic():
    text = "a" * 5000
    chunks = chunk_text(text, chunk_size=1500, overlap=200)
    assert len(chunks) >= 3
    # ensure overlap exists
    assert chunks[0][-50:] != chunks[1][:50]


def test_extract_txt_bytes():
    data = b"Hello world\nThis is a test"
    text = extract_text_from_txt_bytes(data)
    assert "Hello world" in text
