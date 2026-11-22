import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from groq import Groq

from cloud_config import *

app = FastAPI(title="Live RAG Service (Firestore + Gemini + Groq)")

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

class AskRequest(BaseModel):
    question: str
    top_k: int = 1


@app.get("/")
def health_check():
    return {"status": "online"}


@app.post("/ask")
def ask_question(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # 1. Embed user question with RETRIEVAL_QUERY
    emb_resp = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=req.question,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768,
        ),
    )
    query_vec = Vector(emb_resp.embeddings[0].values)

    # 2. Retrieve closest fact(s) from Firestore
    docs = (
        db.collection(COLLECTION_NAME)
        .find_nearest(
            vector_field="embedding",
            query_vector=query_vec,
            distance_measure=DistanceMeasure.COSINE,
            limit=req.top_k,
        )
        .get()
    )

    retrieved_facts = {
            "id": docs[0].id,
            "title": docs[0].to_dict().get("title", ""),
            "text": docs[0].to_dict().get("text", ""),
        }

    print(retrieved_facts)

    context_block = retrieved_facts["text"] # "\n".join([f"- {f['text']}" for f in retrieved_facts])

    # 3. Generate grounded answer via Groq
    chat_completion = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using ONLY the provided context. "
                    "Be concise and accurate. If the context does not contain the answer, say so."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context_block}\n\nQuestion: {req.question}",
            },
        ],
        temperature=0.1,
    )

    return {
        "question": req.question,
        "answer": chat_completion.choices[0].message.content,
        "sources": retrieved_facts,
    }
