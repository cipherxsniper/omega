import uuid
import socket
import time
import hashlib


class NodeIdentityV73:
    def __init__(self):
        self.private_seed = uuid.uuid4().hex
        self.hostname = socket.gethostname()

        self.identity_version = 73
        self.last_rotation = time.time()

        self.node_id = self.generate_identity()

    # 🔁 Auto-regenerating identity (soft rotation)
    def generate_identity(self):
        raw = f"{self.hostname}:{self.private_seed}:{time.time()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    # 🔐 Signed identity hash (verification layer)
    def sign_identity(self):
        payload = self.get_payload()
        raw = str(payload).encode()
        return hashlib.sha256(raw).hexdigest()

    # 🧠 Live refresh cycle (self-updating identity)
    def refresh(self):
        now = time.time()

        # rotate identity every 30 seconds (tunable)
        if now - self.last_rotation > 30:
            self.node_id = self.generate_identity()
            self.last_rotation = now

        return self.node_id

    # 🧾 Identity payload for mesh broadcast
    def get_payload(self):
        return {
            "node_id": self.node_id,
            "hostname": self.hostname,
            "version": self.identity_version,
            "timestamp": time.time(),
            "capabilities": [
                "mesh",
                "cognition",
                "sync",
                "auth"
            ]
        }
