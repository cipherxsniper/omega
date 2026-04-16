import time
import random
import socket
import json


class SwarmIntelligenceV87:
    def __init__(self):
        self.peers = {}
        self.trust = {}
        self.latency = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 6007))
        self.running = True

    # -------------------------
    # PEER MANAGEMENT
    # -------------------------
    def register_peer(self, node_id):
        if node_id not in self.peers:
            self.peers[node_id] = time.time()
            self.trust[node_id] = 1.0
            self.latency[node_id] = random.uniform(10, 100)

    def update_peer(self, node_id):
        self.peers[node_id] = time.time()
        self.trust[node_id] = min(1.0, self.trust.get(node_id, 1.0) + 0.01)

    # -------------------------
    # SCORING ENGINE
    # -------------------------
    def score_peer(self, node_id):
        trust = self.trust.get(node_id, 0.5)
        latency = self.latency.get(node_id, 100)

        score = trust * (100 / (latency + 1))
        return score

    def best_peer(self):
        if not self.peers:
            return None

        return max(self.peers.keys(), key=self.score_peer)

    # -------------------------
    # ROUTING ENGINE
    # -------------------------
    def route(self, payload):
        target = self.best_peer()

        if not target:
            return {"status": "no_peers"}

        score = self.score_peer(target)

        return {
            "status": "routed",
            "target": target,
            "score": score,
            "payload": payload
        }

    # -------------------------
    # LISTENER LOOP
    # -------------------------
    def listen(self):
        print("[V8.7] Swarm Intelligence Layer ONLINE")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                payload = json.loads(data.decode())

                node_id = payload.get("node_id")

                if node_id:
                    self.register_peer(node_id)
                    self.update_peer(node_id)

                print("[RX]", payload)

            except Exception:
                pass

    # -------------------------
    # START SYSTEM
    # -------------------------
    def start(self):
        self.listen()


if __name__ == "__main__":
    SwarmIntelligenceV87().start()
