# Mittelstand Document Agent 📄🇩🇪

![Status](https://img.shields.io/badge/Status-MVP-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Next.js](https://img.shields.io/badge/Next.js-15-black)

**Intelligent Document Analysis for the German Mittelstand.**
A full-stack GenAI application that allows secure, localized extraction, validation, and querying of business PDFs (Invoices, NDAs, Supply Contracts).

## 🏢 The Business Problem

Medium-sized enterprises in Germany ("Mittelstand") process thousands of highly structured and unstructured legal/financial PDFs. Manual data entry is expensive and error-prone. Standard cloud AI solutions pose serious data compliance risks (GDPR, EU AI Act).

**Solution**: This MVP demonstrates a secure, local-first hybrid RAG approach. It extracts structured fields using LLMs, assigns confidence scores to minimize hallucinations, and integrates a "Human-in-the-Loop" (HITL) interface for review.
Running completely locally with Ollama and utilizing **Docker** for strict container isolation guarantees data remains on-premise, adhering to strict German data privacy laws (*Datenschutz*).

---

## 🏗 Architecture

```text
       [ Next.js 15 App Router ]
           |              ^
     JSON  |     SSE      |
    Upload |   Streaming  |
           v              |
      [ FastAPI Backend (Python) ]
           |             |
           |             |   [ BM25 Keyword Search ]
           |             |             ^
           v             v             |
 [ LangChain ] <---> [ Qdrant ] --------
           |
           v
 [ Local Ollama (Llama 3.1 & Nomic Embed) ]
```

---

## ✨ Key Features

1. **Hybrid Search RAG**: Combines Qdrant's semantic embeddings with BM25 keyword search (Reciprocal Rank Fusion) for highly accurate retrieval of German legal text.
2. **Server-Sent Events (SSE)**: Streams AI responses in real-time, just like ChatGPT, creating a responsive user experience.
3. **Structured Data Extraction (HITL)**: Automatically extracts key fields (Invoice Number, Amount, Vendor, etc.) using `with_structured_output`, computes heuristic confidence scores, and visualizes them for human verification.
4. **Source Citations**: AI responses include clickable citations tracing back to exact document chunks and page numbers.
5. **Dynamic i18n UI**: Instantly toggle the UI between English and German, built using `zustand` and Shadcn components.

---

## 🛠 Tech Stack

| Domain | Technology | Use Case |
|---|---|---|
| **Frontend** | Next.js 15, TypeScript, Tailwind | Core framework, routing |
| **UI Library** | Shadcn/ui, Framer Motion | Accessible, enterprise-grade components |
| **Backend** | Python, FastAPI, Pydantic | High-performance API server |
| **AI/LLM** | LangChain, Ollama (Llama 3.1) | RAG orchestration, local inference |
| **Vector DB** | Qdrant (Docker) | Dense vector storage |
| **Sparse DB** | BM25 (`rank_bm25`) | Lexical search enhancement |
| **PDF** | PyMuPDF (`fitz`) | Text extraction handling German umlauts |
| **Containerization** | Docker | Isolated environments for enhanced data security (*Datenschutz*) |

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.11+
- Node.js 22+
- [Ollama](https://ollama.com/) running locally with models: `llama3.1:8b` and `nomic-embed-text`
- Docker Engine *(Optional, but recommended for Qdrant)*

### 1. Vector Database
The application supports two modes for the Qdrant vector database:
- **Local Fallback (No Docker)**: If Docker is not running, the backend will automatically fall back to local persistent storage (`./qdrant_storage`).
- **Docker (Recommended)**: Start the persistent Qdrant service using Docker Compose:
```bash
docker compose up -d
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```
> **Note**: Test PDFs can be generated via `python dummy_pdfs/generate_pdfs.py`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to interact with the application.

---

## 🔮 Future MLOps & Production Path

To transition this MVP to a production-ready enterprise agent, we would implement the following MLOps pipeline:

1. **Model Drift Monitoring**: Implement monitoring tools (e.g., Evidently AI) to track embedding drift over time.
2. **Retrieval Evaluation**: Use frameworks like RAGAS to continuously evaluate Context Precision, Context Recall, and Faithfulness on ground-truth evaluation datasets.
3. **Traceability / Observability**: Full integration with *Pydantic Logfire* or *LangSmith* to log RAG traces, LLM inputs/outputs, and measure latency bottlenecks in production.
4. **Active Learning Feedback Loop**: Implement a system where human corrections made in the HITL Extraction Panel are stored and periodically used to fine-tune a smaller, highly-specialized local model.
5. **Deployment**: Containerize the FastAPI backend and deploy to a managed Kubernetes cluster with GPU node-pools attached to scaled-out Ollama/vLLM inference servers.
