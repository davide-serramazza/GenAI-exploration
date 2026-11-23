# GenAI Exploration: RAG Pipeline with Evaluation Harness

A modular Retrieval-Augmented Generation (RAG) pipeline demonstrating the full ML lifecycle: from document ingestion and embedding to retrieval, generation, and rigorous evaluation. This repository contains **two implementations**: a local, GPU-based version and a cloud-native, serverless version.

[**🔴 Live Demo URL:** ](https://rag-live-service-276396696377.us-central1.run.app/docs#/)

*   `GET /` — Health check
*   `POST /ask` — Query the RAG pipeline

---


## Conceptual Components

The pipeline consists of four core components:

    Knowledge Base and questions (kb.json, questions.json): A collection of 1,000 factual statements, serving as the ground truth for retrieval and a related 50 questions.

    Embedder: Converts text (facts and queries) into high-dimensional vectors. Locally, this is BGE; in the cloud, it is Gemini embeddings.

    Vector Database: Stores the embedded facts and enables similarity search. Locally, this is ChromaDB; in the cloud, it is Firestore.

    LLM (Generator): Takes the user's question and the retrieved context to generate a grounded answer. Locally, this is Qwen2.5-3B; in the cloud, this is Groq.



## Architecture & Design Trade-offs

The key decisions differ between the local and cloud implementations:

*   **Local:** **Lightweight components** ChromaDB for persistent local storage, BGE embeddings and Qwen2.5-3B (4-bit quantized) for GPU inference. This allowed full control over the model and data, but required a **local GPU (4GB)**.
*   **Cloud:** Google Cloud Firestore (native vector search), Gemini embeddings, and Groq for inference. This trades local control for zero infrastructure management, no GPU requirement, and automatic scaling via Cloud Run.

## Evaluation Results

The system was evaluated against a knowledge base of **1,000 automatically sourced facts** (derived from Simple English Wikipedia) and a **50-question test set** generated specifically for this corpus.

*   **Overall Accuracy @ 1:** 100% (50/50)
*   **Overall Accuracy @ 3:** 100% (50/50)
*   **Hallucination Rate:** 0% (based on manual review of generated answers against retrieved context)

*Note: The cloud implementation was benchmarked against the local baseline using the same test set. Results confirmed parity.*


## Tech Stack
*   **Language:** Python
*   **Local:** PyTorch, Hugging Face `transformers`, `sentence-transformers`, ChromaDB
*   **Cloud:** Google Cloud Firestore, Gemini Embeddings, Groq, FastAPI, Cloud Run
*   **MLOps:** MLflow (local), GitHub Actions (CI)

## How to Run (Local)

### Clone & Install

    git clone https://github.com/davide-serramazza/cloud-rag-harness
    cd cloud-rag-harness
    pip install -r local/requirements.txt
    python local/evaluate.py


## Repository Structure

```text
.
├── .github/                 # GitHub Actions CI
│   └── workflows/
│       └── test.yml         # Runs pytest on every push/PR
├── local/                       # Local implementation (ChromaDB + Qwen)
│   ├── tests/                   # Pytest unit tests
│   │   ├── test_rag.py          # Tests for retrieval and generation logic
│   │   └── ...
│   ├── chroma_db.py             # ChromaDB initialization and persistence
│   ├── qwen.py                  # Qwen2.5-3B model loading (4-bit quantization)
│   ├── rag_pipeline.py          # Core RAG logic (retrieval + generation)
│   ├── evaluation.py            # Evaluation harness (Hit@1, Hit@3)
│   ├── evaluate.py              # Entry point to run the local benchmark
│   └── ...
├── cloud/                       # Cloud implementation (Firestore + Gemini + Groq)
│   ├── config.py                # Centralized settings & client init
│   ├── ingest.py                # One-time KB ingestion to Firestore
│   ├── evaluate_cloud.py        # Cloud retrieval benchmark
│   ├── live_app.py              # FastAPI serverless service
│   ├── Dockerfile               # Container build for Cloud Run
│   ├── requirements.txt         # Minimal cloud dependencies
│   └── .dockerignore            # Excludes local cache/secrets from build
├── kb.json                      # 1,000 facts
├── questions.json               # 50 Q&A pairs
└── README.md
