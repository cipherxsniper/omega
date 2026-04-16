# OMEGA MEMORY v3
# Semantic memory layer (FAISS-ready structure)

import json
from pathlib import Path

MEM_FILE = Path("omega_memory.jsonl")

class MemoryStore:

    def store(self, vector_text):
        with open(MEM_FILE, "a") as f:
            f.write(json.dumps({
                "text": vector_text
            }) + "\n")

    def search(self, query):
        if not MEM_FILE.exists():
            return []

        with open(MEM_FILE) as f:
            return f.readlines()[-5:]


MEMORY = MemoryStore()
