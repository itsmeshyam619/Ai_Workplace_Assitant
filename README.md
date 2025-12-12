# AI Workplace Assistant (Minimal RAG)

This project is a minimal, production-ready Retrieval-Augmented Generation (RAG) assistant focused on strict grounding to uploaded documents. It provides a FastAPI backend that ingests PDF/DOCX/TXT files, chunks them, stores embeddings in a local ChromaDB vector store, and serves a simple React + Vite frontend for upload and Q&A.

**Key constraints:** strict context-only answering, no agents, no fine-tuning, small and composable code.

## Tech Stack
- Backend: Python 3.10, FastAPI, Uvicorn
- Embeddings: sentence-transformers (`all-MiniLM-L6-v2`)
- Vector DB: ChromaDB (local persistence)
- LLM: OpenAI GPT-4o-mini (via LangChain ChatOpenAI) — configurable via env
- Frontend: React + Vite + TailwindCSS

## Directory Structure

```
ai-workplace-assistant/
├── backend/
│   ├── main.py
│   ├── services/
│   │   ├── document_reader.py
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   └── rag_pipeline.py
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
		├── src/
		├── package.json
		└── Dockerfile
```

## Local setup (without Docker)

Prerequisites:
- Python 3.10
- Node 20 (for frontend)

Backend

1. Create and activate a virtualenv, then install requirements:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
```

2. Configure env vars in `backend/.env` (set `OPENAI_API_KEY` if using OpenAI).

3. Run the backend:

```bash
# from project root
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend

1. Install dependencies and run dev server:

```bash
cd frontend
npm install
npm run dev
```

The frontend proxies `/api` to the backend (see `vite.config.js`).

## Docker (recommended for quick local setup)

Build and run both services:

```bash
# from project root
docker-compose up --build
```

Services:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

Notes about persistence:
- ChromaDB persists to `backend/vectorstore` (mounted as a bind volume in docker-compose).

## API Endpoints

POST /api/upload
- Accepts multipart file upload (single file): PDF, DOCX, TXT
- Response:

```json
{
	"message": "Document processed successfully",
	"chunks_stored": 48
}
```

POST /api/query
- Body JSON:

```json
{ "question": "What is the leave policy?" }
```

- Response:

```json
{ "answer": "Employees are eligible for 12 days of casual leave per year." }
```

Strict RAG behavior
- The backend constructs a context from the top-3 retrieved chunks, and calls the LLM with a strict prompt:

System message:

```
You are an AI assistant answering questions about workplace documents.
You must use ONLY the provided context to answer.
If the answer is not present in the context, you MUST respond with exactly:
"I could not find that information in the documents."
Do not use prior knowledge. Do not guess. Do not invent facts.
```

User message:

```
Context:
{{context}}

Question: {{question}}

Answer:
```

## Tests

Backend unit tests are under `backend/tests`. Run them with pytest:

```bash
pytest -q
```

## Manual test cases (frontend)

- Upload flow: open Upload page, select a PDF/DOCX/TXT with text, submit, expect success and chunk count.
- Ask flow: open Ask page, enter a question covered in the uploaded documents, submit, expect a grounded answer.
- Error states: Upload unsupported file -> display error; Ask with empty question -> show error; Ask with no documents -> LLM should return fallback string.

## Deployment notes

Render / Railway / Vercel
- Provide environment variables in the platform dashboard: `OPENAI_API_KEY`, `LLM_PROVIDER` (default `openai`), `LLM_MODEL`.
- Ensure persistent storage/mount for `backend/vectorstore` to keep embeddings between restarts.

Example backend start command (Railway/Render):

```
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Example frontend start (Vercel): build and deploy the `frontend/dist` static site.

## Notes and assumptions
- Chunking uses a simple character-based heuristic (1500 chars, 200 overlap) approximating 300–500 tokens.
- LLM provider is selected via env variable `LLM_PROVIDER`. Current implementation uses LangChain `ChatOpenAI` by default; integrating other providers (Groq) can be added in `backend/services/rag_pipeline.py`.
- The system strictly instructs the LLM to return a fallback answer if info is missing; this is the main guard against hallucination.

If you want, I can run tests or start the app in the workspace next.

