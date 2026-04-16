import socket
import threading
import time
import json

from runtime_v7.core.node_identity_v76 import NodeIdentityV76
from runtime_v7.core.cluster_registry_v75 import ClusterRegistryV75
from runtime_v7.core.secure_handshake_v75 import SecureHandshakeV75


class MeshClusterV76:
    def __init__(self, port=6001):
        self.port = port
        self.running = True

        self.identity = NodeIdentityV76()
        self.registry = ClusterRegistryV75()
        self.handshake = SecureHandshakeV75()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

    def broadcast(self):
        while self.running:
            try:
                payload = self.identity.get_payload()
                sig = self.handshake.sign_payload(payload)

                packet = json.dumps({
                    "payload": payload,
                    "sig": sig
                }).encode()

                self.sock.sendto(packet, ("127.0.0.1", self.port))

                self.registry.register(payload["node_id"], sig)

                print({
                    "node": payload["node_id"][:12],
                    "peers": len(self.registry.snapshot())
                })

            except Exception as e:
                print("[V7.6 BROADCAST ERROR]", e)

            time.sleep(2)

    def listen(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(4096)
                packet = json.loads(data.decode())

                payload = packet.get("payload")
                sig = packet.get("sig")

                if not payload:
                    continue

                node_id = payload["node_id"]

                if self.handshake.verify(payload, sig):
                    self.registry.register(node_id, sig)
                    self.registry.heartbeat(node_id)

                    print("[V7.6 RX VERIFIED]", node_id[:12])

            except Exception:
                pass

    def run(self):
        print("[Ω-V7.6] PERSISTENT CLUSTER ONLINE")

        threading.Thread(target=self.broadcast, daemon=True).start()
        threading.Thread(target=self.listen, daemon=True).start()

        while True:
            time.sleep(5)


if __name__ == "__main__":
    MeshClusterV76().run()
