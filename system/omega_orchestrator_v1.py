from system.omega_core_base_v1 import OmegaCoreBaseV1

class OmegaOrchestratorV1(OmegaCoreBaseV1):

    def __init__(self, recursive_engine):
        self.recursive = recursive_engine

    def step(self):
        # ALWAYS SAFE CALL
        rec = self.recursive.step()

        return rec

    def run(self):
        import time

        while True:
            frame = self.safe_step()

            print("[Ω-UKS-1]", frame)

            time.sleep(0.5)
