import os
import subprocess
import time
from collections import defaultdict

class OmegaExecutionGovernorV1:

    def __init__(self):
        self.state = {
            "brains_active": 0,
            "executor_load": 0.0,
            "system_pressure": 0.0
        }

        self.memory = {
            "global_truth": {},
            "last_update": None
        }

        self.brain_votes = []

    # -----------------------------
    # 1. BRAIN ARBITRATION
    # -----------------------------
    def arbitrate_brains(self):
        ps = subprocess.getoutput("ps -A")
        brain_count = ps.lower().count("brain")

        self.state["brains_active"] = brain_count

        # collapse conflict if too many brains
        if brain_count > 8:
            os.system("pkill -f brain_")
            return "collision_resolved"

        return "stable"

    # -----------------------------
    # 2. SYSTEM BUCKET RESOLVER
    # -----------------------------
    def resolve_system_buckets(self, root="~/Omega"):
        root = os.path.expanduser(root)

        buckets = {
            "brain": [],
            "memory": [],
            "executor": [],
            "observer": [],
            "system": [],
            "unknown": []
        }

        for path, dirs, files in os.walk(root):
            for f in files:
                if not f.endswith(".py"):
                    continue

                full = os.path.join(path, f).lower()

                if "brain" in full:
                    buckets["brain"].append(full)
                elif "memory" in full:
                    buckets["memory"].append(full)
                elif "run" in full or "exec" in full:
                    buckets["executor"].append(full)
                elif "observe" in full or "narrate" in full:
                    buckets["observer"].append(full)
                elif "omega" in full:
                    buckets["system"].append(full)
                else:
                    buckets["unknown"].append(full)

        return buckets

    # -----------------------------
    # 3. MEMORY AUTHORITY LAYER
    # -----------------------------
    def update_memory(self, data):
        """
        Single source of truth overwrite model
        """
        self.memory["global_truth"] = data
        self.memory["last_update"] = time.time()

    # -----------------------------
    # 4. EXECUTION GOVERNOR
    # -----------------------------
    def enforce_limits(self):
        ps = subprocess.getoutput("ps -A")

        exec_load = ps.lower().count("python")
        self.state["executor_load"] = exec_load

        # hard safety caps
        if exec_load > 15:
            os.system("pkill -f run_v7")
            os.system("pkill -f run_v723")
            os.system("pkill -f run_v75")

            return "emergency_throttle"

        return "normal"

    # -----------------------------
    # MAIN CONTROL LOOP
    # -----------------------------
    def run(self):
        while True:

            brain_state = self.arbitrate_brains()
            system_map = self.resolve_system_buckets()
            exec_state = self.enforce_limits()

            self.update_memory({
                "brains": self.state["brains_active"],
                "executor_load": self.state["executor_load"],
                "buckets": {k: len(v) for k, v in system_map.items()},
                "brain_state": brain_state,
                "exec_state": exec_state
            })

            print("\n⚡ OMEGA EXECUTION GOVERNOR v1")
            print(self.memory["global_truth"])

            time.sleep(3)


if __name__ == "__main__":
    g = OmegaExecutionGovernorV1()
    g.run()
