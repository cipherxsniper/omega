import time
import traceback

class OmegaSelfHealingKernelV2:

    def __init__(self, engine):
        self.engine = engine
        self.crash_log = []
        self.patches_applied = 0

    # -------------------------
    # SAFE EXECUTION WRAPPER
    # -------------------------
    def safe_step(self):
        try:
            if not hasattr(self.engine, "step"):
                self._auto_patch_step()

            result = self.engine.step()

            return self._normalize(result)

        except Exception as e:
            self.crash_log.append(str(e))
            print("[SHK-2] Crash detected:", e)
            print("[SHK-2] Applying auto-repair...")

            return self._recover_fallback()

    # -------------------------
    # AUTO PATCH STEP METHOD
    # -------------------------
    def _auto_patch_step(self):
        print("[SHK-2] Missing step() detected → patching runtime adapter")

        def fallback_step():
            return {
                "agents": {
                    "brain_0": 0.1,
                    "brain_1": 0.1,
                    "brain_2": 0.1,
                    "brain_3": 0.1
                },
                "strongest": "brain_0",
                "status": "auto-patched",
                "timestamp": time.time()
            }

        setattr(self.engine, "step", fallback_step)
        self.patches_applied += 1

    # -------------------------
    # NORMALIZER (FIXES KEYERRORS)
    # -------------------------
    def _normalize(self, data):
        if not isinstance(data, dict):
            return self._recover_fallback()

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

    # -------------------------
    # EMERGENCY RECOVERY STATE
    # -------------------------
    def _recover_fallback(self):
        return {
            "agents": {
                "brain_0": 0.0,
                "brain_1": 0.0,
                "brain_2": 0.0,
                "brain_3": 0.0
            },
            "strongest": "brain_0",
            "status": "recovered",
            "timestamp": time.time()
        }

    # -------------------------
    # SYSTEM HEALTH REPORT
    # -------------------------
    def health(self):
        return {
            "crashes": len(self.crash_log),
            "patches_applied": self.patches_applied,
            "status": "stable" if len(self.crash_log) < 5 else "degraded"
        }
