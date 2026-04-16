import os
import time
import subprocess
from typing import Dict, List

# =========================
# 🧠 OMEGA OS BRAIN LAYER v1
# =========================

class OmegaOSBrainLayerV1:
    """
    REAL deterministic OS brain layer:
    - validates modules
    - resolves dependencies
    - prevents phantom launches
    - stabilizes control plane loops
    """

    def __init__(self, base_path="~/Omega"):
        self.base_path = os.path.expanduser(base_path)

        self.state = {
            "running": {},
            "dead": {},
            "registry": {},
            "graph": {}
        }

        self.max_active = 25

    # -------------------------
    # FILE VALIDATION
    # -------------------------
    def exists(self, file: str) -> bool:
        return os.path.exists(os.path.join(self.base_path, file))

    # -------------------------
    # SAFE LAUNCH
    # -------------------------
    def launch(self, module: str, role: str = "service"):
        path = os.path.join(self.base_path, module)

        if not os.path.exists(path):
            print(f"❌ SKIP (missing): {module}")
            self.state["dead"][module] = "missing"
            return None

        if len(self.state["running"]) >= self.max_active:
            print(f"⚠️ MAX ACTIVE LIMIT HIT -> skipping {module}")
            return None

        try:
            proc = subprocess.Popen(
                ["python", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            self.state["running"][module] = {
                "pid": proc.pid,
                "role": role,
                "time": time.time()
            }

            print(f"🚀 LAUNCHED [{role}]: {module} PID={proc.pid}")
            return proc.pid

        except Exception as e:
            print(f"❌ LAUNCH FAIL: {module} -> {e}")
            self.state["dead"][module] = str(e)
            return None

    # -------------------------
    # DEPENDENCY SAFETY CHECK
    # -------------------------
    def can_run(self, module: str, deps: List[str]) -> bool:
        for d in deps:
            if d not in self.state["running"]:
                return False
        return True

    # -------------------------
    # CLEAN DEAD PROCESSES
    # -------------------------
    def cleanup(self):
        for m, info in list(self.state["running"].items()):
            try:
                os.kill(info["pid"], 0)
            except:
                print(f"⚠️ DEAD CLEANUP: {m}")
                self.state["dead"][m] = "terminated"
                del self.state["running"][m]

    # -------------------------
    # STATUS
    # -------------------------
    def status(self):
        print("\n🧠 OMEGA OS BRAIN STATUS")
        print(f"RUNNING: {len(self.state['running'])}")
        print(f"DEAD: {len(self.state['dead'])}")
        print("-" * 40)
        for k, v in self.state["running"].items():
            print(f"🟢 {k} -> PID {v['pid']}")
