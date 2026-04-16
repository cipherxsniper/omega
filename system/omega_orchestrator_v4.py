# ============================================================
# OMEGA ORCHESTRATOR v4 — FIXED ENTRY INTERFACE
# GUARANTEED BOOT COMPATIBILITY WITH run_omega_v5.py
# ============================================================

import time


class OmegaOrchestrator:
    def __init__(self):
        self.running = False

    # --------------------------------------------------------
    # REQUIRED ENTRY METHOD (FIXES YOUR ERROR)
    # --------------------------------------------------------

    def run(self):
        print("[ORCH] Omega Orchestrator ONLINE")

        self.running = True

        while self.running:
            try:
                print("[ORCH] tick...")
                time.sleep(2)

            except KeyboardInterrupt:
                print("[ORCH] shutdown signal")
                self.running = False

            except Exception as e:
                print("[ORCH ERROR]", str(e))


# ============================================================
# REQUIRED FUNCTION ENTRY (BACKUP COMPATIBILITY)
# ============================================================

def run():
    OmegaOrchestrator().run()


def OmegaOrchestratorEntry():
    return OmegaOrchestrator()
