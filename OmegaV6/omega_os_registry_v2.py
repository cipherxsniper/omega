import json
import os
import time

class OmegaOSRegistryV2:
    def __init__(self, path="omega_os_registry_v2.json"):
        self.path = path
        self.state = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {
            "services": {},
            "dead": {},
            "history": {}
        }

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)

    def register(self, name):
        self.state["services"].setdefault(name, {
            "restarts": 0,
            "last_seen": time.time(),
            "status": "unknown"
        })
        self.save()

    def mark_dead(self, name):
        self.state["dead"][name] = time.time()
        self.save()

    def heartbeat(self, name):
        if name in self.state["services"]:
            self.state["services"][name]["last_seen"] = time.time()
            self.save()
