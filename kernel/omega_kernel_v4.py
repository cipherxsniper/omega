import os
import time
import subprocess
from collections import defaultdict

class OmegaKernelV4:

    def __init__(self):

        # -----------------------------
        # CORE STATE
        # -----------------------------
        self.state = {
            "tick": 0,
            "stability": 1.0,
            "last_action": None
        }

        # -----------------------------
        # CAUSAL MEMORY GRAPH
        # -----------------------------
        self.causal_graph = defaultdict(list)

        # each entry:
        # node -> [{cause, action, result, tick}]

        self.execution_trace = []

    # -----------------------------
    # PROCESS SCAN
    # -----------------------------
    def scan(self):
        raw = subprocess.getoutput("ps -A")
        return raw.split("\n")

    # -----------------------------
    # CLASSIFY ACTION SOURCES
    # -----------------------------
    def classify(self, processes):
        nodes = {
            "brain": [],
            "executor": [],
            "observer": [],
            "memory": [],
            "system": []
        }

        for p in processes:
            p = p.lower()

            if "brain" in p:
                nodes["brain"].append(p)
            elif "run_" in p or "exec" in p:
                nodes["executor"].append(p)
            elif "observe" in p:
                nodes["observer"].append(p)
            elif "memory" in p:
                nodes["memory"].append(p)
            else:
                nodes["system"].append(p)

        return nodes

    # -----------------------------
    # CAUSAL LINK CREATION
    # -----------------------------
    def record_causal_event(self, cause, action, result):

        event = {
            "tick": self.state["tick"],
            "cause": cause,
            "action": action,
            "result": result
        }

        self.execution_trace.append(event)

        self.causal_graph[cause].append(event)

        self.state["last_action"] = action

    # -----------------------------
    # SIMPLE DECISION ENGINE (CAUSE → EFFECT)
    # -----------------------------
    def decide(self, nodes):

        # simplified causal rule engine

        if len(nodes["executor"]) > 50:
            return "throttle_executors"

        if len(nodes["brain"]) > 8:
            return "reduce_brain_activity"

        if len(nodes["system"]) > 300:
            return "reclassify_system_noise"

        return "maintain_state"

    # -----------------------------
    # APPLY ACTION + TRACE IT
    # -----------------------------
    def apply_action(self, action, nodes):

        result = "noop"

        if action == "throttle_executors":
            os.system("pkill -f run_")
            result = "executors_throttled"

        elif action == "reduce_brain_activity":
            os.system("pkill -f brain_")
            result = "brains_reduced"

        elif action == "reclassify_system_noise":
            result = "system_reclassified"

        else:
            result = "stable"

        self.record_causal_event(
            cause=str(len(nodes)),
            action=action,
            result=result
        )

        return result

    # -----------------------------
    # CAUSAL DRIFT ANALYSIS
    # -----------------------------
    def analyze_drift(self):

        if len(self.execution_trace) < 5:
            return "insufficient_data"

        recent = self.execution_trace[-5:]

        actions = [e["action"] for e in recent]

        if actions.count(actions[0]) == len(actions):
            self.state["stability"] *= 0.95
            return "behavioral_loop_detected"

        return "stable"

    # -----------------------------
    # CAUSAL EXPLANATION ENGINE
    # -----------------------------
    def explain(self):

        if not self.execution_trace:
            return "no_history"

        last = self.execution_trace[-1]

        return {
            "why": f"Triggered because system state matched condition: {last['cause']}",
            "what": last["action"],
            "result": last["result"],
            "tick": last["tick"]
        }

    # -----------------------------
    # MAIN LOOP
    # -----------------------------
    def run(self):

        while True:

            self.state["tick"] += 1

            processes = self.scan()
            nodes = self.classify(processes)

            decision = self.decide(nodes)
            result = self.apply_action(decision, nodes)
            drift = self.analyze_drift()
            explanation = self.explain()

            print("\n🧠 OMEGA KERNEL v4")
            print("TICK:", self.state["tick"])
            print("DECISION:", decision)
            print("RESULT:", result)
            print("DRIFT:", drift)
            print("EXPLANATION:", explanation)

            time.sleep(2)


if __name__ == "__main__":
    k = OmegaKernelV4()
    k.run()
