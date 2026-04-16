import os
import time
import subprocess
from collections import defaultdict

class OmegaKernelV2:

    def __init__(self):
        self.memory = {
            "global_state": {},
            "process_map": {},
            "execution_graph": {},
            "last_tick": None
        }

        self.state = {
            "brain_count": 0,
            "executor_count": 0,
            "system_load": 0,
            "stability": 1.0
        }

    # -----------------------------
    # 1. PROCESS REGISTRY
    # -----------------------------
    def scan_processes(self):
        raw = subprocess.getoutput("ps -A")
        lines = raw.split("\n")

        omega_processes = []

        for line in lines:
            if any(k in line.lower() for k in ["omega", "python", "brain", "run_"]):
                omega_processes.append(line)

        self.state["executor_count"] = len(omega_processes)
        return omega_processes

    # -----------------------------
    # 2. BRAIN ARBITRATION
    # -----------------------------
    def arbitrate_brains(self, processes):
        brain_count = sum(1 for p in processes if "brain" in p.lower())
        self.state["brain_count"] = brain_count

        # conflict resolution
        if brain_count > 6:
            os.system("pkill -f brain_")
            return "brain_collision_resolved"

        return "stable"

    # -----------------------------
    # 3. MEMORY AUTHORITY
    # -----------------------------
    def update_memory(self, processes):
        self.memory["global_state"] = {
            "active_processes": len(processes),
            "brain_count": self.state["brain_count"],
            "executor_count": self.state["executor_count"],
            "stability": self.state["stability"]
        }
        self.memory["last_tick"] = time.time()

    # -----------------------------
    # 4. EXECUTION GRAPH BUILDER
    # -----------------------------
    def build_execution_graph(self, processes):
        graph = defaultdict(list)

        for p in processes:
            p = p.lower()

            if "brain" in p:
                graph["brains"].append(p)
            elif "memory" in p:
                graph["memory"].append(p)
            elif "run_" in p:
                graph["executors"].append(p)
            elif "observer" in p:
                graph["observers"].append(p)
            else:
                graph["system"].append(p)

        self.memory["execution_graph"] = dict(graph)
        return graph

    # -----------------------------
    # 5. STABILITY GOVERNOR
    # -----------------------------
    def enforce_stability(self, processes):
        if len(processes) > 250:
            os.system("pkill -f run_v7")
            os.system("pkill -f run_v723")
            os.system("pkill -f run_v75")

            self.state["stability"] -= 0.2
            return "emergency_shutdown_triggered"

        return "stable"

    # -----------------------------
    # MAIN KERNEL LOOP
    # -----------------------------
    def run(self):
        while True:

            processes = self.scan_processes()

            brain_status = self.arbitrate_brains(processes)
            graph = self.build_execution_graph(processes)
            self.update_memory(processes)
            stability = self.enforce_stability(processes)

            print("\n🧠 OMEGA KERNEL v2")
            print("STATE:", self.memory["global_state"])
            print("GRAPH:", {k: len(v) for k, v in graph.items()})
            print("BRAIN STATUS:", brain_status)
            print("STABILITY:", stability)

            time.sleep(3)


if __name__ == "__main__":
    k = OmegaKernelV2()
    k.run()
