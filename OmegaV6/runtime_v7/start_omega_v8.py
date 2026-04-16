import time
import threading
import hashlib
import hmac
import json
import socket
from collections import defaultdict

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1


class OmegaOSV8:

    def __init__(self):
        print("\n🧠🌍🔐 [OMEGA OS V8] BOOTING EMERGENT COGNITION MESH...\n")

        # -----------------------------
        # CORE SYSTEMS
        # -----------------------------
        self.memory = get_crdt()
        self.semantic = SemanticModelV1()

        # -----------------------------
        # NODE IDENTITY
        # -----------------------------
        self.node_id = self.generate_id()
        self.secret = b"omega-v8-emergent-key"

        # -----------------------------
        # TRUST SYSTEM (ADVANCED)
        # -----------------------------
        self.trust = defaultdict(lambda: 1.0)

        # -----------------------------
        # EMERGENT PATTERN STORE
        # -----------------------------
        self.patterns = []

        # -----------------------------
        # NODE BEHAVIOR TRACKING
        # -----------------------------
        self.behavior_map = defaultdict(list)

        # -----------------------------
        # NETWORK MESH
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
        threading.Thread(target=self.emergence_loop, daemon=True).start()

        print(f"\n🧠 [OMEGA OS V8] ONLINE | node={self.node_id}\n")

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
    # SEMANTIC INTERPRETATION
    # -----------------------------
    def interpret(self, event):
        return self.semantic.interpret(event)

    # -----------------------------
    # BEHAVIOR TRACKING
    # -----------------------------
    def track_behavior(self, node_id, meaning):
        self.behavior_map[node_id].append(meaning)

    # -----------------------------
    # EMERGENT PATTERN DETECTOR
    # -----------------------------
    def detect_patterns(self):
        patterns = []

        entity_counts = defaultdict(int)

        for node, behaviors in self.behavior_map.items():
            for b in behaviors:
                entity = b.get("entity", "unknown")
                entity_counts[entity] += 1

        for entity, count in entity_counts.items():
            if count > 3:
                patterns.append({
                    "pattern_type": "emergent_cluster",
                    "entity": entity,
                    "strength": min(1.0, count / 10),
                    "nodes_involved": len(self.behavior_map)
                })

        return patterns

    # -----------------------------
    # EMERGENCE LOOP (NEW CORE)
    # -----------------------------
    def emergence_loop(self):
        while self.running:
            try:
                patterns = self.detect_patterns()

                for p in patterns:
                    self.patterns.append(p)
                    print(f"[V8 EMERGENCE] {p}")

                time.sleep(3)

            except Exception as e:
                print("[V8 EMERGENCE ERROR]", e)

    # -----------------------------
    # NETWORK LISTENER
    # -----------------------------
    def listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                if not self.verify(event, event.get("signature")):
                    continue

                self.memory.apply(event)

            except Exception:
                pass

    # -----------------------------
    # COGNITION LOOP
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.state["events"]
                new_events = events[self.last_index:]
                self.last_index = len(events)

                for e in new_events:
                    meaning = self.interpret(e)

                    node = e.get("node_id", "self")
                    self.track_behavior(node, meaning)

                    print(f"[V8 COGNITION] {meaning}")

                time.sleep(1)

            except Exception as e:
                print("[V8 COGNITION ERROR]", e)

    # -----------------------------
    # EMIT EVENT
    # -----------------------------
    def emit(self, event):
        event["node_id"] = self.node_id
        event["timestamp"] = time.time()
        event["signature"] = self.sign(event)

        self.memory.apply(event)

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

            print(f"[OMEGA V8] {user}")


if __name__ == "__main__":
    OmegaOSV8().run()
