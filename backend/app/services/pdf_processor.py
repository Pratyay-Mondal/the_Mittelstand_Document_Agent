import fitz
from typing import List, Tuple
from io import BytesIO
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

def process_pdf(file_bytes: bytes, filename: str) -> Tuple[List[Document], int]:
    """
    Extracts text from a PDF and chunks it appropriately for German context.
    Returns:
        - List of LangChain Documents (chunks)
        - Total page count
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    page_count = len(doc)
    
    # Custom German-aware separators
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
    )
    
    chunks = []
    
    for page_num in range(page_count):
        page = doc[page_num]
        text = page.get_text()
        
        # Skip empty pages
        if not text.strip():
            continue
            
        page_chunks = text_splitter.split_text(text)
        
        for i, chunk_text in enumerate(page_chunks):
            chunks.append(
                Document(
                    page_content=chunk_text,
                    metadata={
                        "source_filename": filename,
                        "page_number": page_num + 1,  # 1-indexed
                        "chunk_index": i
                    }
                )
            )
            
    doc.close()
    return chunks, page_count
