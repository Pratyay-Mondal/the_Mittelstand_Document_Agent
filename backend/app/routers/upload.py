import uuid
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.models.schemas import UploadResponse
from app.models.extraction import DocumentState, ExtractionStatus
from app.db.store import store
from app.services.pdf_processor import process_pdf
from app.services.vector_store import index_document
from app.services.extractor import extract_structured_data

router = APIRouter(prefix="/upload", tags=["upload"])

async def background_process(doc_id: str, file_bytes: bytes, filename: str):
    try:
        # 1. Process PDF and Chunk
        chunks, page_count = process_pdf(file_bytes, filename)
        
        # 2. Index to Qdrant & BM25
        index_document(doc_id, chunks)
        
        # 3. Extract structured data (HITL)
        # Combine text from first few pages for extraction to avoid context window explosion
        max_extract_pages = min(3, page_count)
        extract_text = "\n\n".join([c.page_content for c in chunks if c.metadata.get("page_number", 999) <= max_extract_pages])
        
        extraction_result = await extract_structured_data(extract_text)
        
        # 4. Save to Store
        doc_state = DocumentState(
            doc_id=doc_id,
            filename=filename,
            page_count=page_count,
            extraction=extraction_result,
            extraction_status=ExtractionStatus.PENDING
        )
        store.save_doc_state(doc_state)
        
    except Exception as e:
        # Simplistic error handling for MVP
        print(f"Background processing error for {doc_id}: {e}")

@router.post("", response_model=UploadResponse)
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    doc_id = str(uuid.uuid4())
    file_bytes = await file.read()
    
    # Kick off processing in background task to return fast
    background_tasks.add_task(background_process, doc_id, file_bytes, file.filename)
    
    # Save a placeholder state immediately
    store.save_doc_state(DocumentState(
        doc_id=doc_id, 
        filename=file.filename, 
        page_count=0 # Will be updated by bg worker
    ))
    
    return UploadResponse(
        doc_id=doc_id,
        filename=file.filename,
        page_count=0,
        message="Document uploaded and processing started."
    )
