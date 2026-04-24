import os, json, uuid

BRAIN_DIR = "/data/data/com.termux/files/home/Omega/brains"

class OmegaKernel:
    def __init__(self):
        self.nodes = {}
        self.graph = []

    def scan_brains(self):
        brains = os.listdir(BRAIN_DIR)
        self.nodes = {b: {"active": True} for b in brains}
        return self.nodes

    def validate(self, action):
        # safety + structure gate
        allowed = ["CREATE", "CLONE", "MUTATE", "WRITE", "JUMP"]
        return action["type"] in allowed

    def assign_dna(self):
        return str(uuid.uuid4())[:8]

    def approve_transition(self, particle, action):
        if not self.validate(action):
            return False

        particle["dna"] = self.assign_dna()
        particle["node"] = action.get("target", "brain_01")

        self.graph.append({
            "from": particle["id"],
            "to": particle["node"],
            "dna": particle["dna"]
        })

        return True
