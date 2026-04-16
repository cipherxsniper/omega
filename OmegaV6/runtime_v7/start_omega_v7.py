import time
import threading
import hashlib
import hmac
import json
import socket

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1


class OmegaOSV7:

    def __init__(self):
        print("\n🧠🌍🔐 [OMEGA OS V7] BOOTING RECURSIVE INTELLIGENCE ENGINE...\n")

        # -----------------------------
        # CORE SYSTEMS
        # -----------------------------
        self.memory = get_crdt()
        self.semantic = SemanticModelV1()

        # -----------------------------
        # IDENTITY
        # -----------------------------
        self.node_id = self.generate_id()
        self.secret = b"omega-v7-recursive-key"

        # -----------------------------
        # TRUST ECONOMY
        # -----------------------------
        self.trust = {}

        # -----------------------------
        # REASONING RULESET (MUTABLE CORE)
        # -----------------------------
        self.ruleset = {
            "interpret_weight": 1.0,
            "causal_weight": 1.0,
            "novelty_bias": 0.5
        }

        # -----------------------------
        # META-COGNITION STATE
        # -----------------------------
        self.self_model = {
            "thoughts": [],
            "reasoning_patterns": [],
            "reflection_state": []
        }

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
        threading.Thread(target=self.meta_loop, daemon=True).start()

        print(f"\n🧠 [OMEGA OS V7] ONLINE | node={self.node_id}\n")

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
    # REASONING ENGINE (MUTABLE)
    # -----------------------------
    def interpret(self, event):
        base = self.semantic.interpret(event)

        # 🧠 rules actively shape cognition
        base["confidence"] *= self.ruleset["interpret_weight"]

        return base

    # -----------------------------
    # RULE EVOLUTION ENGINE
    # -----------------------------
    def evolve_rules(self, thought):
        if thought.get("confidence", 0) < 0.4:
            self.ruleset["interpret_weight"] *= 0.98

        if thought.get("confidence", 0) > 0.8:
            self.ruleset["interpret_weight"] *= 1.01

    # -----------------------------
    # META-COGNITION LOOP
    # -----------------------------
    def meta_loop(self):
        while self.running:
            try:
                snapshot = {
                    "ruleset": self.ruleset,
                    "trust": self.trust,
                    "memory_size": len(self.memory.state["events"])
                }

                self.self_model["reflection_state"].append(snapshot)

                print(f"[V7 REFLECTION] {snapshot}")

                time.sleep(4)

            except Exception as e:
                print("[V7 META ERROR]", e)

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

                    thought = self.interpret(e)

                    self.self_model["thoughts"].append(thought)

                    self.evolve_rules(thought)

                    print(f"[V7 THOUGHT] {thought}")

                time.sleep(1)

            except Exception as e:
                print("[V7 COGNITION ERROR]", e)

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

            print(f"[OMEGA V7] {user}")


if __name__ == "__main__":
    OmegaOSV7().run()
