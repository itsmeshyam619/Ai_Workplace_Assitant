from pydantic import BaseModel
from typing import List, Any, Dict


class UploadResponse(BaseModel):
    message: str
    chunks_stored: int


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
