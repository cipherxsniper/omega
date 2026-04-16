import os
import time
import subprocess
from collections import defaultdict

class OmegaAttentionControllerV1:

    def __init__(self):
        self.attention_state = {
            "dominant_layer": None,
            "system_load": 0.0,
            "active_processes": 0,
            "brain_pressure": 0.0,
            "executor_pressure": 0.0
        }

        self.role_priority = {
            "brain": 3,
            "observer": 4,
            "memory": 2,
            "executor": 5,
            "system": 1,
            "distributed": 2
        }

    # -----------------------------
    # PROCESS SCAN
    # -----------------------------
    def scan_processes(self):
        ps = subprocess.getoutput("ps -A")
        return ps.split("\n")

    # -----------------------------
    # CLASSIFY SYSTEM PRESSURE
    # -----------------------------
    def classify_pressure(self, process_list):
        counts = defaultdict(int)

        for line in process_list:
            line = line.lower()

            for role in self.role_priority:
                if role in line:
                    counts[role] += 1

        return counts

    # -----------------------------
    # COMPUTE ATTENTION
    # -----------------------------
    def compute_attention(self):
        processes = self.scan_processes()
        counts = self.classify_pressure(processes)

        total = sum(counts.values()) + 1

        self.attention_state["brain_pressure"] = counts["brain"] / total
        self.attention_state["executor_pressure"] = counts["executor"] / total
        self.attention_state["active_processes"] = len(processes)

        # Determine dominant layer
        if counts:
            self.attention_state["dominant_layer"] = max(
                counts.items(),
                key=lambda x: x[1]
            )[0]

        return self.attention_state

    # -----------------------------
    # CONTROL ACTIONS
    # -----------------------------
    def enforce_stability(self):
        """
        Kill duplicate runaway python loops if system overload detected
        """
        if self.attention_state["active_processes"] > 250:
            os.system("pkill -f run_v7")
            os.system("pkill -f run_v723")
            os.system("pkill -f run_v75")

    # -----------------------------
    # MAIN LOOP
    # -----------------------------
    def run(self):
        while True:
            state = self.compute_attention()

            print("\n🧠 OMEGA ATTENTION STATE")
            print(state)

            self.enforce_stability()

            time.sleep(2)


if __name__ == "__main__":
    c = OmegaAttentionControllerV1()
    c.run()
