import threading
import time
from runtime_v7.core.omega_federation_mesh_v1 import FederationMeshV1
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1
from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class OmegaOSV1:
    """
    Omega Operating System V1
    - CRDT Memory Core
    - Federation Mesh Layer
    - Semantic World Model
    - Cognitive Runtime Loop
    """

    def __init__(self):
        print("\n[OMEGA OS V1] INITIALIZING BOOT SEQUENCE...\n")

        # -----------------------------
        # CORE SYSTEMS
        # -----------------------------
        self.memory = get_crdt()
        self.mesh = FederationMeshV1()
        self.semantic = SemanticModelV1()

        self.running = True

        # -----------------------------
        # START BACKGROUND COGNITION
        # -----------------------------
        threading.Thread(target=self.cognition_loop, daemon=True).start()

        print("\n[OMEGA OS V1] ONLINE — COGNITIVE SYSTEM ACTIVE\n")

    # -----------------------------
    # COGNITION ENGINE
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                world = self.semantic.world_state()

                if world:
                    thought = world[-1]
                    print(f"[OMEGA THOUGHT] {thought}")

                time.sleep(2)

            except Exception as e:
                print("[COGNITION ERROR]", e)
                time.sleep(2)

    # -----------------------------
    # USER INTERFACE LOOP
    # -----------------------------
    def run(self):
        while self.running:
            try:
                user = input("\n~Omega$> ").strip()

                if user.lower() == "exit":
                    self.running = False
                    break

                # -------------------------
                # WRITE TO CRDT MEMORY
                # -------------------------
                self.memory.apply({
                    "type": "user_input",
                    "content": user,
                    "timestamp": time.time()
                })

                print(f"[OMEGA] {user}")

            except KeyboardInterrupt:
                self.running = False
                break


# -----------------------------
# BOOT ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    OmegaOSV1().run()
