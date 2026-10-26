"""
evaluation.py


"""
import mlflow

def ask_with_rag(user_query, vectordb, qwen, k=3):
    """Combines Retrieval and Generation."""
    # 1. Retrieve
    results = vectordb.query(user_query, n_results=k)
    retrieved_docs = results['documents'][0]

    # 2. Format Context
    context = "\n".join([f"- {doc}" for doc in retrieved_docs])
    system_prompt = (
        "You are a helpful assistant. Use only the context below to answer the user's question. "
        "If the answer is not in the context, say so clearly. Do not use prior knowledge.\n\n"
        f"Context:\n{context}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ]

    # 3. Generate
    response = qwen.generate_response(messages)

    return response, retrieved_docs

def eval_retrieval(eval_set, vectordb, k=3):
    """Calculates hit rate @ k for the benchmark."""
    results_by_difficulty = {"easy": [], "medium": [], "hard": []}

    for item in eval_set:
        results = vectordb.query(item["question"], n_results=k)

        # Extract integer ID from strings like "fact_12"
        retrieved_ids = [int(id.split("_")[1]) for id in results["ids"][0]]

        hit = item["correct_fact_id"] in retrieved_ids
        results_by_difficulty[item["difficulty"]].append(hit)

    print(f"\nRetrieval hit rate @ {k}:")
    for difficulty, hits in results_by_difficulty.items():
        rate = sum(hits) / len(hits)
        print(f"  {difficulty.upper():8} {rate:.0%}  ({sum(hits)}/{len(hits)})")

    all_hits = [h for hits in results_by_difficulty.values() for h in hits]
    overall_accuracy = sum(all_hits)/len(all_hits)

    # --- MLFLOW LOGGING ---
    # Log the parameters and the final metric
    mlflow.log_param("k_neighbors", k)
    mlflow.log_metric("retrieval_accuracy", overall_accuracy)

    print(f"\n  OVERALL  {overall_accuracy:.0%}  ({sum(all_hits)}/{len(all_hits)})\n")