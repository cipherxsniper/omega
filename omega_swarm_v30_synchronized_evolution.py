import os
import time
import json
import random
import threading
from collections import defaultdict

OMEGA_DIR = os.path.expanduser("~/Omega")

BRAINS = [
    "brain_00",
    "brain_01",
    "brain_02",
    "wink_brain"
]

MEMORY_FILE = "omega_swarm_memory.json"
EVOLUTION_LOG = "omega_swarm_evolution_log.json"


# -----------------------------
# 🧠 SWARM MEMORY CORE
# -----------------------------
class SwarmMemoryV30:
    def __init__(self):
        self.memory = defaultdict(list)

    def write(self, brain, data):
        self.memory[brain].append({
            "t": time.time(),
            "data": data
        })

    def persist(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)


# -----------------------------
# 🧬 SWARM PATCH PROPOSER
# -----------------------------
class SwarmPatchGeneratorV30:
    def propose(self, file_path):
        return {
            "file": file_path,
            "patch": random.choice([
                "reduce_sleep",
                "optimize_loop",
                "improve_logging",
                "no_change_safe"
            ]),
            "risk": random.random()
        }


# -----------------------------
# 🧠 SWARM CONSENSUS ENGINE
# -----------------------------
class SwarmConsensusV30:
    def vote(self, brains, patch):
        votes = {}

        for b in brains:
            # simulated intelligence score
            score = random.random()

            if patch["risk"] < 0.3 and score > 0.4:
                votes[b] = "approve"
            elif patch["risk"] < 0.6:
                votes[b] = "modify"
            else:
                votes[b] = "reject"

        return votes

    def decide(self, votes):
        result = list(votes.values())

        if result.count("approve") > len(result) / 2:
            return "APPLY"
        elif result.count("modify") > result.count("reject"):
            return "MODIFY"
        return "REJECT"


# -----------------------------
# ⚡ SWARM EVOLUTION ENGINE
# -----------------------------
class OmegaSwarmV30:
    def __init__(self):
        self.memory = SwarmMemoryV30()
        self.proposer = SwarmPatchGeneratorV30()
        self.consensus = SwarmConsensusV30()

        self.running = True
        self.step = 0
        self.log = []

    def scan_files(self):
        return [
            f for f in os.listdir(OMEGA_DIR)
            if f.endswith(".py") and "v30" not in f
        ]

    def evolve_file(self, file_name):
        path = os.path.join(OMEGA_DIR, file_name)

        patch = self.proposer.propose(path)
        votes = self.consensus.vote(BRAINS, patch)
        decision = self.consensus.decide(votes)

        self.memory.write(file_name, {
            "patch": patch,
            "votes": votes,
            "decision": decision
        })

        print(f"[v30] {file_name} → {decision}")

        return {
            "file": file_name,
            "patch": patch,
            "votes": votes,
            "decision": decision
        }

    # -----------------------------
    # 🔁 MAIN SWARM LOOP
    # -----------------------------
    def run(self):
        print("[v30] SWARM-WIDE SYNCHRONIZED EVOLUTION ONLINE")

        while self.running:
            self.step += 1

            files = self.scan_files()

            for f in files:
                result = self.evolve_file(f)
                self.log.append(result)

            self.memory.persist()

            with open(EVOLUTION_LOG, "w") as f:
                json.dump(self.log, f, indent=2)

            time.sleep(5)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSwarmV30().run()
