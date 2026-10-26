# GenAI Exploration: RAG Pipeline with MLOps & Evaluation

A self-contained implementation of a retrieval-augmented generation (RAG) pipeline using local models. This project demonstrates not just how to build a RAG system, but how to **evaluate it rigorously** and wrap it in **production-ready MLOps practices**.

The focus is on applying research-grade evaluation methodology to an LLM pipeline, ensuring the system is reproducible, testable, and trackable.

## 🚀 What It Does

1. Loads **Qwen 2.5-3B** locally with 4-bit quantization (runs efficiently on a 4GB GPU).
2. Embeds a 40-fact knowledge base using **BGE-base-en-v1.5**.
3. Stores and retrieves facts via **ChromaDB** (persistent vector store, cosine similarity).
4. Answers questions using retrieved context (RAG).
5. **Evaluates retrieval and faithfulness** on a labeled 15-question benchmark.
6. **Tracks experiments** using MLflow.
7. **Automates testing** via GitHub Actions CI/CD.

## 📊 Evaluation Results

The pipeline was evaluated against a 15-question benchmark (divided into easy, medium, and hard difficulty tiers).

| Metric | Value |
|--------|-------|
| Retrieval hit rate @ 1 | **100%** (15/15) |
| Retrieval hit rate @ 3 | **100%** (15/15) |
| Answer faithfulness | 14/15 grounded, 1/15 correctly declined, 0/15 hallucinated |

**Note on the one failure:** For the question *"How long does it take light to escape the Sun's core?"*, the retriever returned a related but incomplete fact at k=1. Qwen correctly responded that the answer was not in the provided context, rather than hallucinating. This is a positive result for faithfulness, but highlights a retrieval limitation at k=1.

## 🧪 Benchmark Design

The 15 questions are split into three difficulty tiers to reveal *where* and *why* retrieval struggles, rather than just reporting a single aggregate number:

- **Easy (6 questions):** Direct keyword overlap with the target fact.
- **Medium (6 questions):** Paraphrased — same meaning, different words.
- **Hard (3 questions):** Cross-cutting — requires semantic understanding, not keyword matching.

## ⚙️ MLOps & Engineering Practices

This project is built with production-readiness in mind, demonstrating modern software engineering and MLOps practices:

*   **Experiment Tracking:** Integrated **MLflow** to log hyperparameters (`k_neighbors`) and metrics (`retrieval_accuracy`). You can view the runs locally via `mlflow ui`.
*   **Automated Testing (CI/CD):** Integrated **pytest** to validate database ingestion and retrieval logic. Configured **GitHub Actions** (`.github/workflows/test.yml`) to automatically run the test suite on every push.
*   **Object-Oriented Design:** Abstracted the LLM (`qwen.py`) and Vector DB (`chroma_db.py`) into modular classes, separating model infrastructure from RAG logic.
*   **Dynamic Hardware Allocation:** The code automatically detects and utilizes CUDA if available, falling back to CPU for environments without GPUs (like CI runners).

## 🛠️ How to Run Locally

1. Install dependencies: `pip install -r requirements.txt` (ensure `mlflow`, `pytest`, `chromadb`, `transformers`, and `torch` are included).
2. Update the `base_path` in `rag_pipeline.py` to point to your local model and database folders.
3. Run the pipeline: `python rag_pipeline.py`
4. View the metrics dashboard: `mlflow ui` and open `http://localhost:5000`.
5. Run tests locally: `pytest tests/`