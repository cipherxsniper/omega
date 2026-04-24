import os
import json
import random
import uuid

class WorkerAgent:
    def __init__(self, id):
        self.id = id

    def read_file(self, path):
        with open(path, "r") as f:
            return f.read()

    def propose_patch(self, file_path):
        content = self.read_file(file_path)

        # simple mutation logic (symbolic evolution seed)
        mutations = [
            ("function", "fn"),
            ("const", "let"),
            ("true", "1"),
            ("false", "0"),
        ]

        mutated = content
        for a,b in random.sample(mutations, 2):
            mutated = mutated.replace(a,b)

        return {
            "worker_id": self.id,
            "file": file_path,
            "patch_id": str(uuid.uuid4()),
            "original": content,
            "proposed": mutated,
            "confidence": random.random()
        }
