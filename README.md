# GenAI Exploration: RAG Pipeline with Evaluation Harness

A local, modular Retrieval-Augmented Generation (RAG) pipeline designed to demonstrate the full ML lifecycle: from document ingestion and embedding to retrieval, generation, and rigorous evaluation.

The core engineering question this project answers is: **"How do we prove that an LLM system is actually working in production?"**

## Architecture & Design Trade-offs

Instead of building a "demo," this project was built with production constraints in mind. Key decisions include:
*   **Vector Database (ChromaDB):** Chosen for lightweight, persistent local deployment and a straightforward API.
*   **LLM Inference (Qwen2.5-3B):** Implemented with **4-bit quantization** to run on a standard 4GB GPU without sacrificing generation quality.
*   **Embeddings (BGE):** `BAAI/bge-small-en-v1.5` was selected for strong retrieval performance relative to its small size.
*   **Evaluation Harness:** A custom framework to measure **Hit@1** and **Hit@3**, moving beyond "vibes-based" development to quantitative proof of reliability.

## Evaluation Results
The system was evaluated against a knowledge base of **1,000 automatically sourced facts** (derived from Simple English Wikipedia) and a **50-question test set** generated specifically for this corpus.

*   **Overall Accuracy @ 1:** 100% (50/50)
*   **Overall Accuracy @ 3:** 100% (50/50)
*   **Hallucination Rate:** 0% (based on manual review of generated answers against retrieved context)

## Tech Stack
*   **Language:** Python
*   **ML/DL:** PyTorch, Hugging Face `transformers`, `sentence-transformers`
*   **LLM:** Qwen2.5-3B (4-bit quantized)
*   **Vector DB:** ChromaDB
*   **MLOps:** MLflow (Experiment Tracking), pytest, GitHub Actions (CI)

---


## How to Run

1.Clone & Install

    git clone https://github.com/davide-serramazza/GenAI-exploration.git
    cd GenAI-exploration
    pip install -r requirements.txt


2.Run evaluation

    python evaluate.py