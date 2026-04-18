import json
import subprocess
import os

REGISTRY = "omega_node_registry_v63.json"

SAFE_THRESHOLD = 0.7

class ExecutionKernelV7:

    def __init__(self):
        self.registry = self.load_registry()

    def load_registry(self):
        if not os.path.exists(REGISTRY):
            print("❌ Missing registry. Run v6.3 first.")
            return {}

        with open(REGISTRY, "r") as f:
            return json.load(f)

    # -------------------------
    # HEALTH SCORE
    # -------------------------
    def score_node(self, node, data):
        score = 1.0

        # penalize no connections
        if data["connections"] == 0:
            score -= 0.4

        # penalize heavy dependency
        if len(data["depends_on"]) > 5:
            score -= 0.2

        # reward usage
        if len(data["used_by"]) > 3:
            score += 0.2

        return max(0, min(score, 1))

    # -------------------------
    # SELECT SAFE NODES
    # -------------------------
    def select_safe_nodes(self):
        safe = []

        for node, data in self.registry.items():
            if data["type"] != "CORE":
                continue

            score = self.score_node(node, data)

            if score >= SAFE_THRESHOLD:
                safe.append((node, score))

        safe.sort(key=lambda x: x[1], reverse=True)
        return safe

    # -------------------------
    # EXECUTE NODE
    # -------------------------
    def run_node(self, node):
        file = f"{node}.py"

        if not os.path.exists(file):
            return

        try:
            subprocess.Popen(["python", file])
            print(f"🚀 STARTED: {node}")
        except Exception as e:
            print(f"❌ FAILED: {node} -> {e}")

    # -------------------------
    # EXECUTION PHASE
    # -------------------------
    def execute(self):
        print("\n🧠 OMEGA EXECUTION KERNEL v7\n")

        safe_nodes = self.select_safe_nodes()

        print(f"SAFE NODES: {len(safe_nodes)}\n")

        for node, score in safe_nodes[:10]:
            print(f"{node} | score={round(score,2)}")

        print("\n🚀 STARTING SAFE CORE NODES...\n")

        for node, score in safe_nodes[:5]:
            self.run_node(node)

        print("\n🧠 EXECUTION COMPLETE (CONTROLLED MODE)\n")


if __name__ == "__main__":
    kernel = ExecutionKernelV7()
    kernel.execute()
