from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.services.rag_chain import stream_rag_chat
from app.db.store import store

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/stream")
async def chat_stream(doc_id: str, question: str):
    """
    Server-Sent Events endpoint for streaming chat completions
    """
    doc_state = store.get_doc_state(doc_id)
    if not doc_state:
        raise HTTPException(status_code=404, detail="Document not found")
        
    # Log user message
    store.add_chat_message(doc_id, "user", question)
    
    # stream_rag_chat returns an AsyncGenerator formatted as SSE
    return StreamingResponse(
        stream_rag_chat(doc_id, question),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no", # Critical for Nginx
        }
    )

@router.get("/history/{doc_id}")
async def get_chat_history(doc_id: str):
    history = store.get_chat_history(doc_id)
    return {"history": history}
