import socket
import threading
import time
import json

from runtime_v7.core.cluster_registry_v75 import ClusterRegistryV75
from runtime_v7.core.secure_handshake_v75 import SecureHandshakeV75
from runtime_v7.core.secure_mesh_patch_v75 import secure_broadcast, secure_receive


class MeshClusterV75:
    def __init__(self, port=6001):
        self.port = port
        self.broadcast_port = port
        self.running = True

        self.registry = ClusterRegistryV75()
        self.handshake = SecureHandshakeV75()

        self.identity = type("ID", (), {"get_payload": self._identity})()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

    def _identity(self):
        import uuid, socket, time, hashlib
        raw = f"{socket.gethostname()}:{uuid.uuid4().hex}:{time.time()}"
        node_id = hashlib.sha256(raw.encode()).hexdigest()

        return {
            "node_id": node_id,
            "hostname": socket.gethostname(),
            "timestamp": time.time(),
            "type": "omega_v7_5_cluster_node"
        }

    def broadcast_loop(self):
        while self.running:
            try:
                payload = self.identity.get_payload()
                sig = self.handshake.sign_payload(payload)

                packet = json.dumps({
                    "payload": payload,
                    "sig": sig
                }).encode()

                self.sock.sendto(packet, ("127.0.0.1", self.broadcast_port))

                self.registry.register(payload["node_id"], sig)

                print({
                    "node": payload["node_id"][:12],
                    "peers": len(self.registry.snapshot())
                })

            except Exception as e:
                print("[BROADCAST ERROR]", e)

            time.sleep(2)

    def listen_loop(self):
        while self.running:
            try:
                data, _ = self.sock.recvfrom(4096)
                packet = json.loads(data.decode())

                self._handle_rx(packet)

            except Exception:
                pass

    def _handle_rx(self, packet):
        payload = packet.get("payload")
        sig = packet.get("sig")

        if not payload:
            return

        node_id = payload.get("node_id")

        if self.handshake.verify(payload, sig):
            self.registry.register(node_id, sig)
            self.registry.heartbeat(node_id)

            print("[V7.5 RX VERIFIED]", node_id[:12])
        else:
            print("[V7.5 RX REJECTED]")

    def run(self):
        print("[Ω-V7.5] SECURE CLUSTER ONLINE")

        threading.Thread(target=self.broadcast_loop, daemon=True).start()
        threading.Thread(target=self.listen_loop, daemon=True).start()

        while True:
            time.sleep(5)


if __name__ == "__main__":
    MeshClusterV75().run()
