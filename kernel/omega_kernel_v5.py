import os
import time
import subprocess
import random
from collections import defaultdict

class OmegaKernelV5:

    def __init__(self):

        # -----------------------------
        # CORE STATE
        # -----------------------------
        self.state = {
            "tick": 0,
            "stability": 1.0,
            "attention_focus": 0.5
        }

        # -----------------------------
        # POLICY SYSTEM (SELF-ADAPTIVE)
        # -----------------------------
        self.policy = {
            "executor_limit": 50,
            "brain_limit": 8,
            "system_noise_limit": 300,
            "risk_tolerance": 0.5
        }

        # -----------------------------
        # CAUSAL MEMORY
        # -----------------------------
        self.history = []

    # -----------------------------
    # SCAN SYSTEM
    # -----------------------------
    def scan(self):
        raw = subprocess.getoutput("ps -A")
        return raw.split("\n")

    # -----------------------------
    # CLASSIFY SYSTEM
    # -----------------------------
    def classify(self, processes):

        nodes = {
            "brain": [],
            "executor": [],
            "system": []
        }

        for p in processes:
            p = p.lower()

            if "brain" in p:
                nodes["brain"].append(p)
            elif "run_" in p or "exec" in p:
                nodes["executor"].append(p)
            else:
                nodes["system"].append(p)

        return nodes

    # -----------------------------
    # 🔮 PREDICTIVE CAUSAL ENGINE
    # -----------------------------
    def predict(self, nodes):

        futures = []

        # simulate 3 possible outcomes

        for i in range(3):

            exec_factor = len(nodes["executor"]) + random.randint(-5, 5)
            brain_factor = len(nodes["brain"]) + random.randint(-2, 2)
            system_factor = len(nodes["system"]) + random.randint(-20, 20)

            risk = (
                exec_factor * 0.5 +
                brain_factor * 0.3 +
                system_factor * 0.2
            )

            futures.append({
                "scenario": i,
                "risk": risk,
                "exec": exec_factor,
                "brain": brain_factor
            })

        # choose safest predicted path
        best = min(futures, key=lambda x: x["risk"])

        return best, futures

    # -----------------------------
    # ⚡ UNIFIED ATTENTION FIELD
    # -----------------------------
    def attention(self, nodes):

        exec_pressure = len(nodes["executor"])
        brain_pressure = len(nodes["brain"])
        system_pressure = len(nodes["system"])

        focus = (
            exec_pressure * 0.5 +
            brain_pressure * 0.3 +
            system_pressure * 0.2
        )

        # normalize
        self.state["attention_focus"] = min(focus / 100.0, 1.0)

        return self.state["attention_focus"]

    # -----------------------------
    # 🧠 SELF-REWRITING POLICY ENGINE
    # -----------------------------
    def update_policy(self, prediction):

        risk = prediction["risk"]

        # adaptive rule mutation
        if risk > 80:
            self.policy["executor_limit"] -= 5
            self.policy["risk_tolerance"] -= 0.05

        elif risk < 40:
            self.policy["executor_limit"] += 2
            self.policy["risk_tolerance"] += 0.02

        # clamp values
        self.policy["executor_limit"] = max(10, min(200, self.policy["executor_limit"]))
        self.policy["risk_tolerance"] = max(0.1, min(0.9, self.policy["risk_tolerance"]))

    # -----------------------------
    # CAUSAL MEMORY LOGGING
    # -----------------------------
    def log(self, nodes, prediction):

        self.history.append({
            "tick": self.state["tick"],
            "executor_count": len(nodes["executor"]),
            "brain_count": len(nodes["brain"]),
            "predicted_risk": prediction["risk"]
        })

        if len(self.history) > 50:
            self.history.pop(0)

    # -----------------------------
    # MAIN LOOP
    # -----------------------------
    def run(self):

        while True:

            self.state["tick"] += 1

            processes = self.scan()
            nodes = self.classify(processes)

            prediction, futures = self.predict(nodes)
            attention = self.attention(nodes)

            self.update_policy(prediction)
            self.log(nodes, prediction)

            print("\n🧠 OMEGA KERNEL v5")
            print("TICK:", self.state["tick"])
            print("ATTENTION:", self.state["attention_focus"])
            print("PREDICTED FUTURE:", prediction)
            print("POLICY:", self.policy)

            time.sleep(2)


if __name__ == "__main__":
    k = OmegaKernelV5()
    k.run()
