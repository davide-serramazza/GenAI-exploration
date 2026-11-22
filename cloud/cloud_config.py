import os
from google import genai
from google.cloud import firestore

TOP_K = 1  # Retrieve top 3 closest facts to compute Hit@1 and Hit@3

# Raw GitHub URL pointing directly to your knowledge base JSON on the main branch
KB_URL = "https://raw.githubusercontent.com/davide-serramazza/GenAI-exploration/main/kb.json"
QUESTIONS_URL = "https://raw.githubusercontent.com/davide-serramazza/GenAI-exploration/main/questions.json"

# Name of the Firestore collection where facts and vectors will be stored
COLLECTION_NAME = "rag_facts"

# Gemini embedding model and vector size (768 dims saves 75% storage vs 3072)
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 768

# Number of facts to embed and upload per batch (20 batches total for 1,000 facts)
BATCH_SIZE = 20

gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
db = firestore.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"],database="vector-db")

GROQ_MODEL = "openai/gpt-oss-20b"