import time
import random
import json
import threading
import traceback

LOG_FILE = "omega_v13.log"
MEMORY_FILE = "omega_v13_memory.json"

# ---------------------------
# SIMPLE BRAIN CLASS (SAFE)
# ---------------------------
class Brain:
    def __init__(self, name):
        self.name = name
        self.state = random.random()

    def think(self):
        self.state += random.uniform(-0.05, 0.05)
        return {
            "brain": self.name,
            "state": self.state,
            "decision": "explore" if random.random() > 0.5 else "optimize"
        }

# ---------------------------
# OMEGA CORE
# ---------------------------
class OmegaSuperintelligenceV13:
    def __init__(self):
        self.running = True

        # ✅ FIXED (this was your crash zone)
        self.brains = [
            Brain("brain_00"),
            Brain("brain_01"),
            Brain("brain_02"),
            Brain("wink_brain")
        ]

        self.memory = []

    # ---------------------------
    # LOGGING
    # ---------------------------
    def log(self, msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

    # ---------------------------
    # MEMORY SAVE
    # ---------------------------
    def save_memory(self):
        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump(self.memory[-200:], f, indent=2)
        except:
            pass

    # ---------------------------
    # MAIN LOOP
    # ---------------------------
    def run(self):
        self.log("OMEGA V13 ONLINE")

        while self.running:
            try:
                for brain in self.brains:
                    result = brain.think()
                    self.memory.append(result)

                    self.log(f"{result['brain']} → {result['decision']} | {round(result['state'], 4)}")

                self.save_memory()

                time.sleep(1)

            except Exception as e:
                self.log(f"ERROR: {e}")
                self.log(traceback.format_exc())
                time.sleep(2)

# ---------------------------
# AUTO-RESTART WRAPPER
# ---------------------------
def main():
    while True:
        try:
            system = OmegaSuperintelligenceV13()
            system.run()
        except Exception as e:
            print("[FATAL] Restarting system...", e)
            time.sleep(3)

if __name__ == "__main__":
    main()
