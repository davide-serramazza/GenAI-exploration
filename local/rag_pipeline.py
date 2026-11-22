"""
This is the entry point of the application. It should ONLY initialize
dependencies and call functions. (Recommendation: Move the two functions
below into a separate 'evaluation.py' file to keep this file purely as an entry point).
"""

from qwen import QwenChat
from chroma_db import Chromadb
from evaluation import ask_with_rag,eval_retrieval
from os.path import join
import torch
import mlflow
import json

def main():

    base_path = "/media/davide/DATA/qwen/"

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 1. Initialize heavy dependencies
    qwen = QwenChat(join(base_path,"qwen2.5-3B"),device=device)
    vectordb = Chromadb(db_path=join(base_path,"chroma_db"), embedder_path=join(base_path,"bge-base-1.5"),device=device)

    # 2. Setup DB
    with open("../kb.json", "r", encoding="utf-8") as f:
        facts = json.load(f)
    kb = [k['fact'] for k in facts]
    vectordb.populate_collection(kb)

    # 3. Run Benchmark for k = 1 and k = 3
    with open("../questions.json", "r", encoding="utf-8") as f:
        eval_set = json.load(f)
    for k_k in [1,3]:
        with mlflow.start_run(run_name=r"k_{k_k}", nested=True):
            eval_retrieval(eval_set, vectordb, k=k_k)

    # 4. Generate Demo Answers
    for item in eval_set[:3]: # Just do the first 3 to save time
        response, _ = ask_with_rag(item["question"], vectordb, qwen, k=1)
        print(f"Q: {item['question']}\nA: {response}\n")

if __name__ == '__main__':
    main()