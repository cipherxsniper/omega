import time
import threading
import hashlib
import hmac
import json
import socket

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1


class OmegaOSV5:

    def __init__(self):
        print("\n🧠🌍 [OMEGA OS V5] BOOTING CAUSAL INTELLIGENCE MESH...\n")

        # -----------------------------
        # CORE SYSTEMS
        # -----------------------------
        self.memory = get_crdt()
        self.semantic = SemanticModelV1()

        # -----------------------------
        # IDENTITY
        # -----------------------------
        self.node_id = self.generate_id()
        self.secret = b"omega-v5-causal-key"

        # -----------------------------
        # TRUST / REPUTATION SYSTEM
        # -----------------------------
        self.reputation = {}
        self.causal_accuracy = {}

        # -----------------------------
        # CAUSAL GRAPH MEMORY
        # -----------------------------
        self.causal_graph = []

        # -----------------------------
        # WAN MESH (LOCAL START)
        # -----------------------------
        self.peers = ["127.0.0.1:6100"]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 6100))

        self.running = True
        self.last_index = 0

        # -----------------------------
        # THREADS
        # -----------------------------
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.cognition_loop, daemon=True).start()

        print(f"\n🧠 [OMEGA OS V5] ONLINE | node={self.node_id}\n")

    # -----------------------------
    # IDENTITY
    # -----------------------------
    def generate_id(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

    def sign(self, event):
        raw = json.dumps(event, sort_keys=True).encode()
        return hmac.new(self.secret, raw, hashlib.sha256).hexdigest()

    def verify(self, event, signature):
        return hmac.compare_digest(self.sign(event), signature)

    # -----------------------------
    # CAUSAL ENGINE (NEW CORE)
    # -----------------------------
    def infer_causal_relation(self, event, meaning):
        return {
            "cause": event.get("type", "unknown"),
            "effect": meaning.get("action", "state_change"),
            "confidence": meaning.get("confidence", 0.5),
            "node": self.node_id,
            "timestamp": time.time()
        }

    # -----------------------------
    # REPUTATION UPDATE
    # -----------------------------
    def update_reputation(self, node_id, causal_event):
        score = causal_event.get("confidence", 0.5)

        if node_id not in self.reputation:
            self.reputation[node_id] = 1.0

        # reward accurate causality, penalize weak
        self.reputation[node_id] *= (0.95 + score * 0.1)

    # -----------------------------
    # NETWORK LISTENER
    # -----------------------------
    def listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                sig = event.get("signature")
                if not sig:
                    continue

                if not self.verify(event, sig):
                    continue

                # trust filter
                node = event.get("node_id", "unknown")
                if self.reputation.get(node, 1.0) < 0.3:
                    continue

                self.memory.apply(event)

            except Exception:
                pass

    # -----------------------------
    # BROADCAST
    # -----------------------------
    def broadcast(self, event):
        raw = json.dumps(event).encode()

        for peer in self.peers:
            try:
                ip, port = peer.split(":")
                self.sock.sendto(raw, (ip, int(port)))
            except Exception:
                pass

    # -----------------------------
    # COGNITION LOOP (CAUSAL)
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.state["events"]
                new_events = events[self.last_index:]
                self.last_index = len(events)

                for e in new_events:

                    meaning = self.semantic.interpret(e)
                    causal = self.infer_causal_relation(e, meaning)

                    self.causal_graph.append(causal)

                    print(f"[V5 CAUSAL] {causal}")

                    # update reputation
                    self.update_reputation(e.get("node_id", "self"), causal)

                time.sleep(1)

            except Exception as e:
                print("[V5 COGNITION ERROR]", e)

    # -----------------------------
    # EMIT EVENT
    # -----------------------------
    def emit(self, event):
        event["node_id"] = self.node_id
        event["timestamp"] = time.time()
        event["signature"] = self.sign(event)

        self.memory.apply(event)
        self.broadcast(event)

    # -----------------------------
    # CLI
    # -----------------------------
    def run(self):
        while True:
            user = input("\n~Omega$> ").strip()

            if user.lower() == "exit":
                break

            self.emit({
                "type": "user_input",
                "content": user
            })

            print(f"[OMEGA V5] {user}")


if __name__ == "__main__":
    OmegaOSV5().run()
