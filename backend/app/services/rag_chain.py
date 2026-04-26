from typing import List, AsyncGenerator
import json
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.config import settings
from app.services.vector_store import get_retriever

PROMPT_TEMPLATE = """
You are a highly efficient document analysis assistant for business documents.
Answer the question using ONLY the provided context.
Be EXTREMELY concise and direct. Do not use redundant words, filler phrases, or introductory sentences.
Provide only the factual answer.
Answer in the same language as the user's question (usually English or German).
If you don't know the answer, just say that you don't know. 
Always cite your sources with [Page X] format based on the context metadata.

Context:
{context}

Question: {question}

Answer:
"""

def _format_docs(docs: List[Document]) -> str:
    formatted = []
    for d in docs:
        page = d.metadata.get("page_number", "?")
        formatted.append(f"--- [Page {page}] ---\n{d.page_content}")
    return "\n\n".join(formatted)

async def stream_rag_chat(doc_id: str, question: str) -> AsyncGenerator[str, None]:
    retriever = get_retriever(doc_id)
    
    llm = ChatOllama(
        base_url=settings.ollama_base_url,
        model=settings.ollama_chat_model,
        temperature=0.3,
    )
    
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Retrieve docs up front so we can send sources at the end
    docs = retriever.invoke(question)
    
    chain = prompt | llm | StrOutputParser()
    
    # Stream the tokens
    async for chunk in chain.astream({"context": _format_docs(docs), "question": question}):
        yield f"data: {json.dumps({'token': chunk, 'type': 'token'})}\n\n"
        
    # Send done event with sources
    sources = []
    seen_pages = set()
    for d in docs:
        page = d.metadata.get("page_number", 1)
        if page not in seen_pages:
            seen_pages.add(page)
            sources.append({
                "page": page,
                "chunk_index": d.metadata.get("chunk_index", 0),
                "text_snippet": d.page_content[:150] + "..."
            })
            if len(sources) >= 3: # top 3 unique pages
                break
        
    yield f"data: {json.dumps({'type': 'done', 'sources': sources})}\n\n"
