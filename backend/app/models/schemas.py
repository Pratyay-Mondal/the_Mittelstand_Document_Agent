from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    page_count: int
    message: str

class ChatRequest(BaseModel):
    question: str
    
class Citation(BaseModel):
    page: int
    chunk_index: int
    text_snippet: str

class ChatEventToken(BaseModel):
    token: str
    type: str = "token"

class ChatEventDone(BaseModel):
    type: str = "done"
    sources: List[Citation]
