"""
Vector Database Wrapper.

This class manages the ChromaDB persistent client and the embedding function.
It abstracts away the complexity of turning text into vectors and querying them.
"""

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class Chromadb:
    def __init__(self, db_path, embedder_path,device):
        # PersistentClient saves the DB to disk so we don't re-embed the KB on every run
        self.client = chromadb.PersistentClient(path=db_path)

        self.device = device

        self.embedding_function = SentenceTransformerEmbeddingFunction(
            embedder_path,
            device=self.device
        )

        # Use Cosine similarity for text embeddings
        self.collection = self.client.get_or_create_collection(
            name="my_knowledge_base",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )

    def populate_collection(self, kb):
        # Upsert allows us to run this multiple times without creating duplicates
        ids = [f"fact_{i}" for i in range(len(kb))]
        self.collection.upsert(documents=kb, ids=ids)
        print(f"Collection now contains {self.collection.count()} documents.")

    def query(self, query_text, n_results=3):
        # Returns the top-k most similar documents
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )