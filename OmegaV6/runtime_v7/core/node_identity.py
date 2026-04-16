import uuid
import socket
import time


class NodeIdentity:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created = time.time()
        self.hostname = socket.gethostname()

    def get_payload(self):
        return {
            "node_id": self.id,
            "hostname": self.hostname,
            "timestamp": time.time(),
            "capabilities": [
                "mesh",
                "cognition",
                "sync"
            ],
            "type": "omega_v7_2_node"
        }
