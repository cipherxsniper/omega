import json
import os
import time
import random

class IdentityPersistenceFieldV62:
    def __init__(self, path="omega_identity_field_v6.json"):
        self.path = path
        self.state = self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except:
                pass

        return {
            "clusters": {},
            "tick": 0
        }

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)

    def update_cluster(self, cluster_id, strength_delta):
        clusters = self.state["clusters"]

        if cluster_id not in clusters:
            clusters[cluster_id] = {
                "strength": 0.5,
                "age": 0,
                "last_seen": time.time()
            }

        c = clusters[cluster_id]

        # 🧠 persistence reinforcement
        c["strength"] += strength_delta
        c["age"] += 1
        c["last_seen"] = time.time()

        # clamp stability
        c["strength"] = max(0.0, min(2.0, c["strength"]))

    def decay(self):
        now = time.time()

        for cid, c in self.state["clusters"].items():
            time_gap = now - c["last_seen"]

            # slow decay instead of deletion
            decay = time_gap * 0.0001

            c["strength"] -= decay
            c["strength"] = max(0.1, c["strength"])  # never fully dies

    def step(self, active_clusters):
        self.state["tick"] += 1

        for c in active_clusters:
            self.update_cluster(c, strength_delta=0.05)

        self.decay()
        self.save()

        return self.state
