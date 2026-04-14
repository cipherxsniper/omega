from system.omega_contract_v10 import OmegaContractV10

class SafeOmegaEngineV10:
    def __init__(self, engine):
        self.engine = engine

        # AUTO PATCH missing step()
        if not hasattr(self.engine, "step"):
            def fallback_step():
                return {
                    "agents": getattr(self.engine, "agents", {"brain_0": 1.0}),
                    "status": "patched",
                    "metrics": {"fallback": True}
                }
            self.engine.step = fallback_step

    def step(self):
        try:
            raw = self.engine.step()
        except Exception as e:
            raw = {
                "agents": {"brain_0": 1.0},
                "status": f"recovered:{type(e).__name__}",
                "metrics": {}
            }

        return OmegaContractV10.normalize(raw)
