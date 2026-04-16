import time
import threading
import hashlib
import hmac
import json
import socket
from collections import defaultdict

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1


class OmegaOSV9:

    def __init__(self):
        print("\n🧠🌍🔐 [OMEGA OS V9] BOOTING SELF-GENERATING COGNITION ARCHITECTURE...\n")

        # -----------------------------
        # CORE SYSTEMS
        # -----------------------------
        self.memory = get_crdt()
        self.semantic = SemanticModelV1()

        # -----------------------------
        # IDENTITY
        # -----------------------------
        self.node_id = self.generate_id()
        self.secret = b"omega-v9-self-gen-key"

        # -----------------------------
        # TRUST / ECONOMY
        # -----------------------------
        self.trust = defaultdict(lambda: 1.0)
        self.reputation = defaultdict(float)

        # -----------------------------
        # REASONING MODULE REGISTRY (NEW CORE)
        # -----------------------------
        self.reasoning_modules = []

        # -----------------------------
        # EMERGENT PATTERNS (FROM V8)
        # -----------------------------
        self.patterns = []

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
        threading.Thread(target=self.module_generation_loop, daemon=True).start()

        print(f"\n🧠 [OMEGA OS V9] ONLINE | node={self.node_id}\n")

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
    # MODULE GENERATION (CORE V9 FEATURE)
    # -----------------------------
    def generate_reasoning_module(self, pattern):
        module = {
            "type": pattern.get("pattern_type", "generic"),
            "weight": pattern.get("strength", 0.5),
            "logic": lambda x: {"processed": True, "input": x},
            "created_at": time.time()
        }

        self.reasoning_modules.append(module)

        print(f"[V9 MODULE CREATED] {module}")

    # -----------------------------
    # APPLY REASONING MODULES
    # -----------------------------
    def apply_modules(self, event):
        results = []

        for m in self.reasoning_modules:
            try:
                result = m["logic"](event)
                results.append(result)
            except Exception:
                pass

        return results

    # -----------------------------
    # MODULE GENERATION LOOP
    # -----------------------------
    def module_generation_loop(self):
        while self.running:
            try:
                for p in self.patterns:
                    if p not in self.reasoning_modules:
                        self.generate_reasoning_module(p)

                time.sleep(5)

            except Exception as e:
                print("[V9 MODULE ERROR]", e)

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
                    meaning = self.semantic.interpret(e)

                    print(f"[V9 MEANING] {meaning}")

                    # feed into pattern space (simplified)
                    self.patterns.append({
                        "pattern_type": meaning.get("entity", "unknown"),
                        "strength": meaning.get("confidence", 0.5)
                    })

                    # apply generated reasoning modules
                    outputs = self.apply_modules(e)

                    if outputs:
                        print(f"[V9 MODULE OUTPUT] {outputs}")

                time.sleep(1)

            except Exception as e:
                print("[V9 COGNITION ERROR]", e)

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

            print(f"[OMEGA V9] {user}")


if __name__ == "__main__":
    OmegaOSV9().run()
