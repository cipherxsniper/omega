from runtime_v7.core.v9_9_swarm_bus import SwarmBusV99
from runtime_v7.core.v9_8_shared_memory_swarm_core import get_memory
import socket, json, hmac, hashlib

class EncryptedIdentityMeshV92:
    def __init__(self, port=6012):
        self.memory = get_memory()
        self.bus = SwarmBusV99()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))

        self.key = b"OMEGA_SWARM_KEY_V9"

    def verify(self, msg):
        sig = msg.get("sig")
        raw = {k: msg[k] for k in msg if k != "sig"}

        expected = hmac.new(
            self.key,
            json.dumps(raw, sort_keys=True).encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(sig, expected)

    def start(self):
        print("[V9.2] EVENT IDENTITY MESH ONLINE")

        while True:
            data, addr = self.sock.recvfrom(4096)
            msg = json.loads(data.decode())

            if not self.verify(msg):
                continue

            node_id = msg["node_id"]

            self.memory.mark_trusted(node_id)

            # 🔥 EMIT TRUST EVENT INTO BUS
            self.bus.emit({
                "type": "node_trusted",
                "node_id": node_id
            })

if __name__ == "__main__":
    EncryptedIdentityMeshV92().start()
