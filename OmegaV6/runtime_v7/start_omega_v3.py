import time
import threading
import hashlib
import hmac
import json

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt
from runtime_v7.core.omega_federation_mesh_v1 import FederationMeshV1
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1


class OmegaOSV3:

    def __init__(self):
        print("\n[OMEGA OS V3] INITIALIZING RECURSIVE COGNITION ENGINE...\n")

        self.memory = get_crdt()
        self.mesh = FederationMeshV1()
        self.semantic = SemanticModelV1()

        self.running = True

        # -----------------------------
        # RECURSIVE RULESET (EVOLVING)
        # -----------------------------
        self.rules = {
            "confidence_boost": 1.0,
            "novelty_bias": 0.5,
            "pattern_memory_weight": 1.0
        }

        # -----------------------------
        # CRYPTO IDENTITY
        # -----------------------------
        self.node_id = self.generate_id()
        self.secret = b"omega-v3-secret-key"

        self.last_index = 0

        threading.Thread(target=self.cognition_loop, daemon=True).start()

        print(f"[OMEGA OS V3] ONLINE | node={self.node_id}\n")

    # -----------------------------
    # NODE IDENTITY
    # -----------------------------
    def generate_id(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

    def sign(self, event):
        raw = json.dumps(event, sort_keys=True).encode()
        return hmac.new(self.secret, raw, hashlib.sha256).hexdigest()

    def verify(self, event, signature):
        expected = self.sign(event)
        return hmac.compare_digest(expected, signature)

    # -----------------------------
    # RECURSIVE COGNITION ENGINE
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.state["events"]
                new_events = events[self.last_index:]
                self.last_index = len(events)

                for e in new_events:
                    thought = self.semantic.interpret(e)

                    # 🧠 RULE INFLUENCE (recursive cognition)
                    thought["confidence"] *= self.rules["confidence_boost"]

                    print(f"[OMEGA THOUGHT V3] {thought}")

                    # 🧠 SELF-ADAPTATION HOOK
                    self.evolve_rules(thought)

                time.sleep(1)

            except Exception as e:
                print("[V3 COGNITION ERROR]", e)

    # -----------------------------
    # RULE EVOLUTION
    # -----------------------------
    def evolve_rules(self, thought):
        if thought.get("confidence", 0) < 0.5:
            self.rules["confidence_boost"] *= 0.99  # reduce bias

        if thought.get("confidence", 0) > 0.8:
            self.rules["confidence_boost"] *= 1.001  # reinforce patterns

    # -----------------------------
    # SECURE EVENT APPLY
    # -----------------------------
    def emit_event(self, event):
        event["_id"] = self.node_id
        event["signature"] = self.sign(event)

        self.memory.apply(event)

        self.mesh.broadcast(event)

    # -----------------------------
    # CLI
    # -----------------------------
    def run(self):
        while True:
            user = input("\n~Omega$> ").strip()

            if user.lower() == "exit":
                break

            event = {
                "type": "user_input",
                "content": user,
                "node_id": self.node_id,
                "timestamp": time.time()
            }

            self.emit_event(event)

            print(f"[OMEGA V3] {user}")


if __name__ == "__main__":
    OmegaOSV3().run()
