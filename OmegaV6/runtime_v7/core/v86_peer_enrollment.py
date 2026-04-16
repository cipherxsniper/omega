import time
import json
import socket
import hashlib


class PeerEnrollmentV86:
    def __init__(self, identity, registry):
        self.identity = identity
        self.registry = registry
        self.pending = {}

    # -------------------------
    # 📡 CREATE ENROLL REQUEST
    # -------------------------
    def create_enroll_request(self):
        payload = {
            "node_id": self.identity.node_id,
            "hostname": socket.gethostname(),
            "timestamp": time.time(),
            "type": "enroll_request"
        }

        signature = hashlib.sha256(
            str(payload).encode()
        ).hexdigest()

        return {
            "payload": payload,
            "sig": signature
        }

    # -------------------------
    # 🤝 VERIFY INCOMING REQUEST
    # -------------------------
    def verify_request(self, packet):
        payload = packet.get("payload")
        sig = packet.get("sig")

        expected = hashlib.sha256(str(payload).encode()).hexdigest()

        return sig == expected

    # -------------------------
    # 🧠 HANDLE ENROLLMENT
    # -------------------------
    def handle_enroll(self, packet):
        if not self.verify_request(packet):
            return False

        node_id = packet["payload"]["node_id"]

        self.registry.register(node_id)
        self.pending[node_id] = time.time()

        print(f"[V8.6] NODE ENROLLED: {node_id[:12]}")

        return True
