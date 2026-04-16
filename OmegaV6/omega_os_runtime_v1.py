import time
import json
import os

STATE_FILE = "omega_runtime_state.json"

class OmegaOSRuntimeV1:
    def __init__(self):
        self.state = self.load()

    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE) as f:
                    return json.load(f)
            except:
                pass
        return {
            "services": {},
            "health": "green",
            "tick": 0
        }

    def save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def register(self, name):
        self.state["services"][name] = {
            "status": "active",
            "last_seen": time.time()
        }

    def heartbeat(self, name):
        if name in self.state["services"]:
            self.state["services"][name]["last_seen"] = time.time()

    def check_health(self):
        now = time.time()
        dead = []

        for k, v in self.state["services"].items():
            if now - v["last_seen"] > 10:
                dead.append(k)

        if dead:
            self.state["health"] = "degraded"
        else:
            self.state["health"] = "green"

        return dead

    def loop(self):
        while True:
            self.state["tick"] += 1
            dead = self.check_health()

            if dead:
                print(f"⚠️ DEAD SERVICES: {dead}")

            self.save()
            time.sleep(2)

if __name__ == "__main__":
    runtime = OmegaOSRuntimeV1()
    runtime.loop()
