# GenAI Exploration: RAG Pipeline with Evaluation

A small, self-contained exploration of retrieval-augmented generation (RAG) using local models. This project builds a minimal RAG pipeline over a 40-fact knowledge base and, more importantly, **evaluates it rigorously** — measuring retrieval accuracy and answer faithfulness.

The focus is not on building a production system, but on applying research-grade evaluation methodology to an LLM pipeline.

## What It Does

1. Loads **Qwen 2.5-3B** locally with 4-bit quantization (runs on a 4GB GPU)
2. Embeds a 40-fact knowledge base using **BGE-base-en-v1.5**
3. Stores and retrieves facts via **ChromaDB** (persistent vector store, cosine similarity)
4. Answers questions using retrieved context (RAG)
5. **Evaluates retrieval and faithfulness** on a labeled 15-question benchmark

## Results

| Metric | Value |
|--------|-------|
| Retrieval hit rate @ 1 | **100%** (15/15) |
| Retrieval hit rate @ 1 — easy | 100% (6/6) |
| Retrieval hit rate @ 1 — medium | 100% (6/6) |
| Retrieval hit rate @ 1 — hard | 100% (3/3) |
| Answer faithfulness | 14/15 grounded, 1/15 correctly declined, 0/15 hallucinated |

**Note on the one failure:** For the question *"How long does it take light to escape the Sun's core?"*, the retriever returned a related but incomplete fact at k=1. Qwen correctly responded that the answer was not in the provided context, rather than hallucinating. This is a positive result for faithfulness, but it highlights a retrieval limitation at k=1.

## Benchmark Design

The 15 questions are split into three difficulty tiers:

- **Easy (6 questions):** Direct keyword overlap with the target fact.
- **Medium (6 questions):** Paraphrased — same meaning, different words.
- **Hard (3 questions):** Cross-cutting — requires semantic understanding, not keyword matching.

This tiering reveals where retrieval succeeds and where it struggles, rather than reporting a single aggregate number.