import json
import os
import time
import threading

STATE_FILE = "omega_swarm_memory_v6.json"
LOCK_FILE = "omega_v6.lock"


class PersistentMemory:
    def __init__(self):
        self.state = {
            "ticks": 0,
            "events": [],
            "last_heartbeat": None
        }
        self.load()

    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    self.state = json.load(f)
                print("[V6 MEMORY] Loaded previous swarm state")
            except:
                print("[V6 MEMORY] Corrupted state → resetting")

    def save(self):
        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.state, f)
        os.replace(tmp, STATE_FILE)

    def log_event(self, event):
        self.state["events"].append(event)

        # prevent unlimited growth
        self.state["events"] = self.state["events"][-200:]

        self.save()


class SwarmV6:
    def __init__(self):
        self.memory = PersistentMemory()
        self.running = True

    def heartbeat_loop(self):
        while self.running:
            self.memory.state["ticks"] += 1

            event = {
                "type": "heartbeat",
                "tick": self.memory.state["ticks"],
                "time": time.time()
            }

            self.memory.state["last_heartbeat"] = event
            self.memory.log_event(event)

            print(f"[V6] tick {event['tick']} | persisted")

            time.sleep(2)

    def run(self):
        print("[V6 SWARM] Persistent Memory Swarm ONLINE")

        t = threading.Thread(target=self.heartbeat_loop)
        t.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[V6] Shutting down...")
            self.running = False
            self.memory.save()


if __name__ == "__main__":
    SwarmV6().run()
