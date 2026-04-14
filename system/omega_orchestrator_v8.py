# ============================================================
# OMEGA ORCHESTRATOR v8 — FINAL STABLE INTELLIGENCE BINDER
# FIXED: learning integration + convergence loop + safe brains
# ============================================================

import time
import traceback


class OmegaOrchestrator:

    def __init__(self):
        self.running = False

        # CORE SYSTEMS
        self.mesh = None
        self.memory = None
        self.economy = None
        self.learning = None
        self.meta = None
        self.convergence = None

        self.brains = []

    # ============================================================
    # 🧠 INITIALIZE CORE SYSTEMS
    # ============================================================

    def initialize_core(self):
        print("[ORCH-v8] Initializing core systems...")

        from omega_event_mesh_v5 import OmegaEventMesh
        from omega_global_memory_cloud_v9 import OmegaGlobalMemoryCloud
        from omega_intelligence_economy_v10 import OmegaIntelligenceEconomy
        from omega_learning_engine_v11 import OmegaLearningEngine
        from omega_meta_brain_v10 import OmegaMetaBrain
        from omega_learning_convergence_v12 import OmegaLearningConvergenceV12

        self.mesh = OmegaEventMesh()
        self.memory = OmegaGlobalMemoryCloud()

        self.economy = OmegaIntelligenceEconomy(self.mesh, self.memory)

        # 🧠 MUST exist before brains
        self.learning = OmegaLearningEngine()

        self.meta = OmegaMetaBrain(self.economy, self.mesh)

        # 🔁 NEW: adaptive convergence system
        self.convergence = OmegaLearningConvergenceV12(
            self.mesh,
            self.memory,
            self.learning,
            self.economy
        )

        print("[ORCH-v8] Core systems ONLINE")

    # ============================================================
    # 🧠 LOAD BRAINS (UNIFIED INTERFACE)
    # ============================================================

    def load_brains(self):
        print("[ORCH-v8] Loading brains...")

        try:
            from Brain_00_v10 import Brain00
            from Brain_11_v10 import Brain11
            from Brain_22_v10 import Brain22
            from ParallelBrain import ParallelBrain

            # ALL BRAINS MUST MATCH:
            # (mesh, memory, learning_engine)

            self.brains = [
                Brain00(self.mesh, self.memory, self.learning),
                Brain11(self.mesh, self.memory, self.learning),
                Brain22(self.mesh, self.memory, self.learning),
                ParallelBrain(self.mesh, self.memory, self.learning)
            ]

            print(f"[ORCH-v8] brains loaded: {len(self.brains)}")

        except Exception as e:
            print("[ORCH-v8] brain load error:", str(e))
            traceback.print_exc()

    # ============================================================
    # 🔗 SYSTEM BINDING
    # ============================================================

    def bind_system(self):
        print("[ORCH-v8] Binding swarm network...")

        # register brains into economy
        for i, _ in enumerate(self.brains):
            self.economy.register_agent(f"brain_{i}")

        self.mesh.publish(
            "system_start",
            {"status": "online", "brains": len(self.brains)},
            source="orchestrator_v8"
        )

        print("[ORCH-v8] system bound successfully")

    # ============================================================
    # 🧠 META EVALUATION (SAFE)
    # ============================================================

    def meta_cycle(self):
        try:
            report = self.meta.evaluate_swarm()
            self.meta.rebalance()
            return report

        except Exception as e:
            return {
                "status": "safe_mode",
                "error": str(e)
            }

    # ============================================================
    # 🔁 MAIN LOOP (FULL INTELLIGENCE FLOW)
    # ============================================================

    def run(self):
        self.initialize_core()
        self.load_brains()
        self.bind_system()

        self.running = True
        print("[ORCH-v8] OMEGA FULL SYSTEM ONLINE")

        tick = 0

        while self.running:
            try:
                # -----------------------------
                # EVENT BROADCAST
                # -----------------------------
                self.mesh.publish(
                    "system_tick",
                    {"tick": tick},
                    source="orchestrator_v8"
                )

                # -----------------------------
                # META EVALUATION (SAFE)
                # -----------------------------
                if tick % 5 == 0:
                    report = self.meta_cycle()
                    print("[ORCH-v8] swarm:", report)

                # -----------------------------
                # 🧠 LEARNING INGESTION
                # -----------------------------
                self.learning.ingest({
                    "tick": tick,
                    "brains": len(self.brains)
                })

                # -----------------------------
                # 🔁 ADAPTIVE CONVERGENCE STEP
                # -----------------------------
                if tick % 3 == 0:
                    conv = self.convergence.step()
                    print("[ORCH-v8] convergence:", conv["observation"])

                tick += 1
                time.sleep(2)

            except KeyboardInterrupt:
                print("[ORCH-v8] shutdown requested")
                self.running = False

            except Exception as e:
                print("[ORCH-v8 ERROR]", str(e))
                traceback.print_exc()


# ============================================================
# ENTRYPOINTS
# ============================================================

def run():
    OmegaOrchestrator().run()


def OmegaOrchestratorEntry():
    return OmegaOrchestrator()
