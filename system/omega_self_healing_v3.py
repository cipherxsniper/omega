import time
import types

class OmegaSelfHealingKernelV3:

    def __init__(self, engine):
        self.engine = engine
        self.rewrites = 0
        self.failures = 0

    # -----------------------------
    # MAIN SAFE ENTRY
    # -----------------------------
    def safe_step(self):
        self._ensure_contract()

        try:
            result = self.engine.step()
            return self._normalize(result)

        except Exception as e:
            self.failures += 1
            print("[SHK-3] Failure detected:", e)
            return self._emergency_rewrite()

    # -----------------------------
    # CONTRACT ENFORCEMENT LAYER
    # -----------------------------
    def _ensure_contract(self):
        if not hasattr(self.engine, "step") or not callable(getattr(self.engine, "step")):
            print("[SHK-3] Missing step() → generating runtime implementation")
            self._inject_step()

    # -----------------------------
    # AUTO METHOD GENERATION
    # -----------------------------
    def _inject_step(self):

        def generated_step():
            return {
                "agents": {
                    "brain_0": 0.5,
                    "brain_1": 0.5,
                    "brain_2": 0.5,
                    "brain_3": 0.5
                },
                "strongest": "brain_0",
                "status": "auto_rewritten",
                "timestamp": time.time()
            }

        self.engine.step = types.MethodType(generated_step, self.engine)
        self.rewrites += 1

    # -----------------------------
    # NORMALIZATION LAYER
    # -----------------------------
    def _normalize(self, data):

        if not isinstance(data, dict):
            return self._emergency_rewrite()

        if "agents" not in data:
            data["agents"] = {
                "brain_0": 0.0,
                "brain_1": 0.0,
                "brain_2": 0.0,
                "brain_3": 0.0
            }

        if "strongest" not in data:
            try:
                data["strongest"] = max(data["agents"], key=data["agents"].get)
            except:
                data["strongest"] = "brain_0"

        if "status" not in data:
            data["status"] = "healed"

        if "timestamp" not in data:
            data["timestamp"] = time.time()

        return data

    # -----------------------------
    # EMERGENCY REWRITE STATE
    # -----------------------------
    def _emergency_rewrite(self):
        return {
            "agents": {
                "brain_0": 0.0,
                "brain_1": 0.0,
                "brain_2": 0.0,
                "brain_3": 0.0
            },
            "strongest": "brain_0",
            "status": "reconstructed",
            "timestamp": time.time()
        }

    # -----------------------------
    # SYSTEM HEALTH REPORT
    # -----------------------------
    def health(self):
        return {
            "rewrites": self.rewrites,
            "failures": self.failures,
            "state": "stable" if self.failures < 10 else "degrading"
        }
