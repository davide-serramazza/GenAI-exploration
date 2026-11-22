import time
import requests
from google import genai
from google.genai import types
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure

from cloud_config import *

def retrieve_top_k(question_text: str, k: int = TOP_K) -> list[str]:
    """Embeds a question and returns the top-k matching document IDs from Firestore."""
    # Use RETRIEVAL_QUERY to match the RETRIEVAL_DOCUMENT vectors in Firestore
    response = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question_text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIM,
        ),
    )
    query_vector = Vector(response.embeddings[0].values)

    # Query Firestore using Cosine similarity
    collection = db.collection(COLLECTION_NAME)
    vector_query = collection.find_nearest(
        vector_field="embedding",
        query_vector=query_vector,
        distance_measure=DistanceMeasure.COSINE,
        limit=k,
    )

    results = vector_query.get()
    return [doc.id for doc in results]


def evaluate():
    """Downloads questions.json from GitHub """
    print(f"Downloading knowledge base from: {QUESTIONS_URL}")
    resp = requests.get(QUESTIONS_URL, timeout=30)
    resp.raise_for_status()  # Raises an error immediately if the URL fails (e.g., 404)
    questions = resp.json()

    print(questions[0].keys())

    hit_at_1=0
    for idx, item in enumerate(questions):
        # Adjust field names if your questions.json uses different keys
        question = item["question"]
        correct_id = str(item["source_fact_id"])
        retrieved_ids = retrieve_top_k(question, k=TOP_K)

        is_hit_1 = retrieved_ids[0] == correct_id if retrieved_ids else False
        hit_at_1 += is_hit_1

        status = "✅" if is_hit_1 else "❌"
        print(f"[{idx+1}/{len(questions)}] {status} Expected: {correct_id} | Retrieved: {retrieved_ids}")

        # Gentle pause (~60 RPM) to stay well within Free Tier rate limits
        time.sleep(1.0)

    total = len(questions)
    print("\n" + "=" * 50)
    print(f"Hit@1 Accuracy: {hit_at_1}/{total} ({hit_at_1 / total:.1%})")
    print("=" * 50) # stay within the minute quota


if __name__ == "__main__":
    evaluate()