import threading
import time
import hashlib

from runtime_v7.core.omega_federation_mesh_v1 import FederationMeshV1
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1
from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class OmegaOSV2:
    """
    Omega OS V2:
    - Fixed cognition loop (no spam cycles)
    - Federation-ready sync layer
    - Trust + identity hash layer
    - Early recursive cognition hooks
    """

    def __init__(self):
        print("\n[OMEGA OS V2] BOOTING EVOLUTIONARY SYSTEM...\n")

        self.memory = get_crdt()
        self.mesh = FederationMeshV1()
        self.semantic = SemanticModelV1()

        self.running = True

        # 🧠 FIX: memory cursor prevents infinite replay
        self.last_index = 0

        # 🧠 thought memory (prevents duplicate prints)
        self.thought_cache = set()

        # 🔐 identity seed
        self.node_id = self.generate_id()

        threading.Thread(target=self.cognition_loop, daemon=True).start()

        print(f"\n[OMEGA OS V2] ONLINE | node={self.node_id}\n")

    # -----------------------------
    # IDENTITY SYSTEM
    # -----------------------------
    def generate_id(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

    # -----------------------------
    # COGNITION ENGINE (FIXED)
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.state["events"]

                # ONLY PROCESS NEW EVENTS
                new_events = events[self.last_index:]
                self.last_index = len(events)

                for e in new_events:
                    thought = self.semantic.interpret(e)

                    key = str(thought)

                    # avoid repeating identical thoughts
                    if key in self.thought_cache:
                        continue

                    self.thought_cache.add(key)

                    print(f"[OMEGA THOUGHT] {thought}")

                time.sleep(1)

            except Exception as e:
                print("[COGNITION ERROR]", e)
                time.sleep(2)

    # -----------------------------
    # CLI INTERFACE
    # -----------------------------
    def run(self):
        while self.running:
            try:
                user = input("\n~Omega$> ").strip()

                if user.lower() == "exit":
                    self.running = False
                    break

                # inject structured event
                self.memory.apply({
                    "type": "user_input",
                    "content": user,
                    "node_id": self.node_id,
                    "timestamp": time.time()
                })

                print(f"[OMEGA] {user}")

            except KeyboardInterrupt:
                self.running = False
                break


if __name__ == "__main__":
    OmegaOSV2().run()
