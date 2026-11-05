import pytest
from chroma_db import Chromadb
from kb import kb

def test_chroma_retrieval():
    """
    Test that the vector database can ingest facts and retrieve the correct one.
    We use a temporary directory for the test DB so it doesn't overwrite the real one.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize DB with a tiny embedding model (downloads automatically) on CPU
        db = Chromadb(db_path=tmpdir, embedder_path="BAAI/bge-small-en-v1.5",device="cpu")
        db.populate_collection(kb)

        # Query for Cleopatra
        results = db.query("Who was Cleopatra?", n_results=1)

        # Assert that we got exactly 1 result back
        assert len(results['documents'][0]) == 1

        # Assert that the top result is indeed the Cleopatra fact
        assert "Cleopatra" in results['documents'][0][0]