import os
import json
import time
import uuid
import socket
import hashlib

class NodeIdentityV76:
    def __init__(self, path="runtime_v7/core/.node_identity.json"):
        self.path = path
        self.hostname = socket.gethostname()

        self.identity = self.load_or_create()

    def create_identity(self):
        seed = uuid.uuid4().hex
        raw = f"{self.hostname}:{seed}".encode()
        node_id = hashlib.sha256(raw).hexdigest()

        return {
            "node_id": node_id,
            "hostname": self.hostname,
            "created": time.time(),
            "version": 76,
            "capabilities": ["mesh", "cognition", "sync"]
        }

    def load_or_create(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except:
                pass

        identity = self.create_identity()
        self.save(identity)
        return identity

    def save(self, identity=None):
        identity = identity or self.identity
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        with open(self.path, "w") as f:
            json.dump(identity, f, indent=2)

    def get_payload(self):
        self.identity["timestamp"] = time.time()
        return self.identity
