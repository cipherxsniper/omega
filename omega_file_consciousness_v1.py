import os
import subprocess
import time

class OmegaFileConsciousnessV1:

    def __init__(self, root="~/Omega"):
        self.root = os.path.expanduser(root)
        self.index = {}
        self.runtime_map = {}

    # ---------- FILE SCAN ----------
    def scan(self):
        files = []

        for root, dirs, fs in os.walk(self.root):
            for f in fs:
                if f.endswith(".py"):
                    full = os.path.join(root, f)
                    files.append(full)

        return files

    # ---------- ROLE TAGGING ----------
    def tag(self, filename):
        f = filename.lower()

        if "memory" in f:
            return "memory"
        if "observer" in f or "narrate" in f:
            return "observer"
        if "run" in f or "start" in f or "main" in f:
            return "executor"
        if "brain" in f or "cognitive" in f:
            return "brain"
        if "swarm" in f or "mesh" in f:
            return "distributed"
        return "system"

    # ---------- BUILD INDEX ----------
    def build_index(self):
        files = self.scan()

        for f in files:
            self.index[f] = {
                "role": self.tag(f),
                "active": self.is_running(f)
            }

        return self.index

    # ---------- CHECK RUNTIME ----------
    def is_running(self, file):
        try:
            result = subprocess.getoutput(f"pgrep -f {file}")
            return bool(result.strip())
        except:
            return False

    # ---------- COGNITION MAP ----------
    def cognition_map(self):
        summary = {}

        for f, meta in self.index.items():
            role = meta["role"]
            summary.setdefault(role, {"count": 0, "active": 0})

            summary[role]["count"] += 1
            if meta["active"]:
                summary[role]["active"] += 1

        return summary

    # ---------- HUMAN READABLE VIEW ----------
    def report(self):
        self.build_index()
        cmap = self.cognition_map()

        return {
            "total_files": len(self.index),
            "cognition_map": cmap,
            "active_processes": sum(1 for x in self.index.values() if x["active"])
        }
