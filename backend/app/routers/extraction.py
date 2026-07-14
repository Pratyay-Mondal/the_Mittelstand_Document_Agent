from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.extraction import DocumentState, DocumentExtraction, ExtractionStatus
from app.db.store import store
from app.services.extractor import extract_structured_data

router = APIRouter(prefix="/extraction", tags=["extraction"])

@router.get("/{doc_id}", response_model=DocumentState)
async def get_extraction(doc_id: str):
    doc_state = store.get_doc_state(doc_id)
    if not doc_state:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc_state

@router.put("/{doc_id}")
async def update_extraction(doc_id: str, extraction: DocumentExtraction):
    """Save user-reviewed extraction data."""
    doc_state = store.get_doc_state(doc_id)
    if not doc_state:
        raise HTTPException(status_code=404, detail="Document not found")
        
    doc_state.extraction = extraction
    doc_state.extraction_status = ExtractionStatus.APPROVED
    store.save_doc_state(doc_state)
    
    return {"message": "Extraction updated and approved successfully."}

@router.post("/{doc_id}/re-extract")
async def trigger_re_extraction(doc_id: str, background_tasks: BackgroundTasks):
    doc_state = store.get_doc_state(doc_id)
    if not doc_state:
        raise HTTPException(status_code=404, detail="Document not found")
    
    chunks = store.get_chunks(doc_id)
    if not chunks:
        raise HTTPException(status_code=400, detail="Cannot re-extract, no chunks found.")
        
    async def _re_extract_bg():
        try:
            doc_state.extraction_status = ExtractionStatus.PENDING
            store.save_doc_state(doc_state)
            
            max_extract_pages = min(3, doc_state.page_count or 1)
            extract_text = "\n\n".join([c.page_content for c in chunks if c.metadata.get("page_number", 999) <= max_extract_pages])
            
            extraction_result = await extract_structured_data(extract_text)
            
            doc_state.extraction = extraction_result
            store.save_doc_state(doc_state)
        except Exception as e:
            print(f"Re-extraction error: {e}")
            
    background_tasks.add_task(_re_extract_bg)
    return {"message": "Re-extraction triggered in background."}
