import logging
from typing import List
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers.ensemble import EnsembleRetriever

from app.config import settings
from app.db.store import store

logger = logging.getLogger(__name__)

# Initialize Qdrant Client — try Docker first, fall back to local persistent mode
_using_local_qdrant = False
try:
    client = QdrantClient(url=settings.qdrant_url, timeout=3)
    client.get_collections()  # test connectivity
    logger.info(f"Connected to Qdrant Docker at {settings.qdrant_url}")
except Exception as e:
    logger.warning(f"Qdrant Docker not reachable ({e}), falling back to local storage at '{settings.qdrant_local_path}'")
    client = QdrantClient(path=settings.qdrant_local_path)
    _using_local_qdrant = True


def _get_embeddings():
    return OllamaEmbeddings(
        base_url=settings.ollama_base_url,
        model=settings.ollama_embed_model,
    )


def index_document(doc_id: str, chunks: List[Document]):
    """
    Indexes the chunks using both Qdrant (dense) and BM25 (sparse/in-memory).
    """
    embeddings = _get_embeddings()

    # 1. Index in Qdrant Vector Store
    # We create a new collection per document for absolute isolation.
    if _using_local_qdrant:
        QdrantVectorStore.from_documents(
            chunks,
            embeddings,
            path=settings.qdrant_local_path,
            collection_name=f"doc_{doc_id}",
        )
    else:
        QdrantVectorStore.from_documents(
            chunks,
            embeddings,
            url=settings.qdrant_url,
            collection_name=f"doc_{doc_id}",
        )

    # 2. Store chunks for BM25 retriever
    store.save_chunks(doc_id, chunks)
    logger.info(f"Indexed {len(chunks)} chunks for doc {doc_id}")


def get_retriever(doc_id: str, k: int = 5):
    """
    Returns a Hybrid Retriever combining Qdrant dense search with BM25 keyword search
    via Reciprocal Rank Fusion (EnsembleRetriever).
    """
    embeddings = _get_embeddings()

    # 1. Qdrant dense retriever
    if _using_local_qdrant:
        qdrant_vs = QdrantVectorStore(
            client=QdrantClient(path=settings.qdrant_local_path),
            collection_name=f"doc_{doc_id}",
            embedding=embeddings,
        )
    else:
        qdrant_vs = QdrantVectorStore(
            client=client,
            collection_name=f"doc_{doc_id}",
            embedding=embeddings,
        )
    qdrant_retriever = qdrant_vs.as_retriever(search_kwargs={"k": k})

    # 2. BM25 sparse retriever
    chunks = store.get_chunks(doc_id)
    if not chunks:
        # Fall back to dense-only if no chunks stored
        logger.warning(f"No chunks in store for BM25, using dense-only for doc {doc_id}")
        return qdrant_retriever

    bm25_retriever = BM25Retriever.from_documents(chunks, k=k)

    # 3. Ensemble (Reciprocal Rank Fusion)
    ensemble = EnsembleRetriever(
        retrievers=[bm25_retriever, qdrant_retriever],
        weights=[settings.bm25_weight, settings.qdrant_weight],
    )
    logger.info(f"Hybrid retriever created for doc {doc_id} (BM25={settings.bm25_weight}, Qdrant={settings.qdrant_weight})")
    return ensemble
