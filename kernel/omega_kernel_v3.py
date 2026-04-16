import os
import time
import subprocess
from collections import defaultdict

class OmegaKernelV3:

    def __init__(self):

        self.state = {
            "tick": 0,
            "cpu_pressure": 0.0,
            "consensus_strength": 1.0,
            "active_slice": None
        }

        self.agents = {
            "brains": [],
            "executors": [],
            "observers": [],
            "memory": [],
            "system": []
        }

        self.consensus = {
            "brain_votes": [],
            "agreement_ratio": 1.0
        }

        self.schedule = []

    # -----------------------------
    # PROCESS SCAN
    # -----------------------------
    def scan(self):
        raw = subprocess.getoutput("ps -A")
        lines = raw.split("\n")

        classified = defaultdict(list)

        for line in lines:
            l = line.lower()

            if "brain" in l:
                classified["brains"].append(l)
            elif "run_" in l or "exec" in l:
                classified["executors"].append(l)
            elif "observe" in l:
                classified["observers"].append(l)
            elif "memory" in l:
                classified["memory"].append(l)
            else:
                classified["system"].append(l)

        self.agents = dict(classified)
        return self.agents

    # -----------------------------
    # BRAIN CONSENSUS ENGINE
    # -----------------------------
    def brain_consensus(self):

        brains = self.agents.get("brains", [])

        if not brains:
            self.consensus["agreement_ratio"] = 0.0
            return "no_brains"

        # simulate voting signals
        votes = []

        for b in brains:
            vote = 1 if hash(b) % 2 == 0 else -1
            votes.append(vote)

        agreement = sum(1 for v in votes if v == 1) / len(votes)

        self.consensus["brain_votes"] = votes
        self.consensus["agreement_ratio"] = agreement

        if agreement < 0.5:
            self.state["consensus_strength"] *= 0.8
            return "conflict"

        return "aligned"

    # -----------------------------
    # SCHEDULER ENGINE
    # -----------------------------
    def build_schedule(self):

        self.schedule = []

        priorities = {
            "executors": 4,
            "brains": 3,
            "memory": 2,
            "observers": 1,
            "system": 0
        }

        for role, items in self.agents.items():
            for item in items:
                self.schedule.append((role, item, priorities.get(role, 0)))

        self.schedule.sort(key=lambda x: x[2], reverse=True)

        return self.schedule

    # -----------------------------
    # TIME SLICER
    # -----------------------------
    def execute_slice(self):

        if not self.schedule:
            return "idle"

        role, item, priority = self.schedule[0]

        self.state["active_slice"] = {
            "role": role,
            "process": item,
            "priority": priority
        }

        return self.state["active_slice"]

    # -----------------------------
    # STABILITY ADJUSTMENT
    # -----------------------------
    def adjust_stability(self):

        if self.consensus["agreement_ratio"] < 0.4:
            os.system("pkill -f brain_")
            self.state["consensus_strength"] *= 0.7

    # -----------------------------
    # MAIN LOOP
    # -----------------------------
    def run(self):

        while True:

            self.state["tick"] += 1

            self.scan()
            consensus = self.brain_consensus()
            self.build_schedule()
            active = self.execute_slice()
            self.adjust_stability()

            print("\n🧠 OMEGA KERNEL v3")
            print("TICK:", self.state["tick"])
            print("CONSENSUS:", consensus)
            print("AGREEMENT:", self.consensus["agreement_ratio"])
            print("ACTIVE SLICE:", active)
            print("BRAIN COUNT:", len(self.agents.get("brains", [])))
            print("EXEC COUNT:", len(self.agents.get("executors", [])))

            time.sleep(2)


if __name__ == "__main__":
    k = OmegaKernelV3()
    k.run()
