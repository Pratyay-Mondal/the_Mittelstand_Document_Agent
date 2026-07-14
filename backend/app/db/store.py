import threading
from typing import Dict, Any, List
from langchain_core.documents import Document
from app.models.extraction import DocumentState

class InMemoryStore:
    def __init__(self):
        self._lock = threading.Lock()
        # doc_id -> DocumentState
        self._docs: Dict[str, DocumentState] = {}
        # doc_id -> list of raw text chunks for BM25
        self._chunks: Dict[str, List[Document]] = {}
        # doc_id -> list of dicts {"role": "user"|"ai", "content": str}
        self._chat_history: Dict[str, List[Dict[str, str]]] = {}

    def save_doc_state(self, doc_state: DocumentState):
        with self._lock:
            self._docs[doc_state.doc_id] = doc_state

    def get_doc_state(self, doc_id: str) -> DocumentState | None:
        with self._lock:
            return self._docs.get(doc_id)

    def save_chunks(self, doc_id: str, chunks: List[Document]):
        with self._lock:
            self._chunks[doc_id] = chunks

    def get_chunks(self, doc_id: str) -> List[Document]:
        with self._lock:
            return self._chunks.get(doc_id, [])
    
    def add_chat_message(self, doc_id: str, role: str, content: str):
        with self._lock:
            if doc_id not in self._chat_history:
                self._chat_history[doc_id] = []
            self._chat_history[doc_id].append({"role": role, "content": content})
            
    def get_chat_history(self, doc_id: str) -> List[Dict[str, str]]:
        with self._lock:
            return self._chat_history.get(doc_id, [])

# Global instance for the app
store = InMemoryStore()
