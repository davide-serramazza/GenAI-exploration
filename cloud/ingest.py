import os
import time
import requests
from google import genai
from google.genai import types
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from evaluate_cloud import *

def fetch_facts(url: str) -> list[dict]:

    """Downloads kb.json from GitHub """
    print(f"Downloading knowledge base from: {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()  # Raises an error immediately if the URL fails (e.g., 404)
    raw_data = resp.json()

    facts = []

    for idx, item in enumerate(raw_data):
        text = item["fact"]
        doc_id = str(item['id'])
        title = item['title']
        facts.append({"id": doc_id, "text": text, "title":[title]})

    return facts



def ingest():
    facts = fetch_facts(KB_URL)
    print(f"Loaded {len(facts)} facts. Starting ingestion...\n")

    collection = db.collection(COLLECTION_NAME)

    for i in range(800, len(facts), BATCH_SIZE):
        batch_facts = facts[i : i + BATCH_SIZE]
        texts = [f["text"] for f in batch_facts]

        # Embed 50 facts at once using Gemini
        response = gemini_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=EMBEDDING_DIM,
            ),
        )

        # Write 50 documents + vectors to Firestore in one batch
        fs_batch = db.batch()
        for fact_obj, emb_obj in zip(batch_facts, response.embeddings):
            doc_ref = collection.document(fact_obj["id"])
            fs_batch.set(
                doc_ref,
                {
                    "title": fact_obj["title"],
                    "text": fact_obj["text"],
                    "embedding": Vector(emb_obj.values),
                },
            )
        fs_batch.commit()

        print(f"[{min(i + BATCH_SIZE, len(facts))}/{len(facts)}] Uploaded batch...")
        # stay within the free quota!
        time.sleep(21)

    print("\nDone! All 1,000 facts are now in Firestore.")

if __name__ == "__main__":
    ingest()