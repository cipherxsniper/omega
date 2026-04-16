import socket
import threading
import json
import time


class MeshClusterV862Runner:
    def __init__(self, port=6001):
        self.port = port
        self.running = True
        self.peers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        print(f"[V8.6.2] RUNNER ONLINE on port {self.port}", flush=True)

    # ---------------- RX ----------------
    def listen(self):
        print("[V8.6.2 RX] listener started", flush=True)

        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                payload = json.loads(data.decode())

                node_id = payload.get("node_id")

                if node_id:
                    self.peers[node_id] = time.time()

                print("[V8.6.2 RX]", payload, flush=True)

            except Exception as e:
                print("[V8.6.2 RX ERROR]", e, flush=True)

    # ---------------- TX ----------------
    def broadcast(self):
        print("[V8.6.2 TX] broadcaster started", flush=True)

        while self.running:
            try:
                payload = {
                    "node_id": "local_node",
                    "type": "heartbeat",
                    "timestamp": time.time()
                }

                data = json.dumps(payload).encode()

                self.sock.sendto(data, ("127.0.0.1", self.port))

                print("[V8.6.2 TX] sent heartbeat", flush=True)

            except Exception as e:
                print("[V8.6.2 TX ERROR]", e, flush=True)

            time.sleep(3)

    # ---------------- RUNNER ----------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.broadcast, daemon=True)

        t1.start()
        t2.start()

        print("[V8.6.2] SYSTEM LOOP ACTIVE", flush=True)

        # 🔥 CRITICAL: prevents Termux exit
        while True:
            time.sleep(5)


if __name__ == "__main__":
    MeshClusterV862Runner().start()
