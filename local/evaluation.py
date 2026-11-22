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
    n_corrects = 0

    for item in eval_set:
        results = vectordb.query(item["question"], n_results=k)

        # Extract integer ID from strings like "fact_12"
        retrieved_ids = [int(id.split("_")[1]) for id in results["ids"][0]]

        hit = item["source_fact_id"] in retrieved_ids
        if hit:
            n_corrects+=1
    overall_accuracy = n_corrects/len(eval_set)

    # --- MLFLOW LOGGING ---
    # Log the parameters and the final metric
    mlflow.log_param("k_neighbors", k)
    mlflow.log_metric("retrieval_accuracy", overall_accuracy)

    print(f"\n  OVERALL ACCURACY @ {k} IS , {overall_accuracy} : {n_corrects}/{len(eval_set)}")