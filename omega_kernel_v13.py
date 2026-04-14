import os
import subprocess
import time
import json

OMEGA_DIR = os.path.expanduser("~/Omega")
STATE_FILE = "omega_self_model_v13.json"


# -------------------------
# SELF MODEL ENGINE
# -------------------------
class OmegaSelfModelV13:
    def __init__(self):
        self.process_map = {}
        self.active_modules = []
        self.conflicts = []
        self.tick = 0

    # -------------------------
    # SCAN SYSTEM
    # -------------------------
    def scan_files(self):
        files = os.listdir(OMEGA_DIR)

        omega_files = [
            f for f in files
            if f.startswith("omega_") and f.endswith(".py")
        ]

        self.active_modules = omega_files

        return omega_files

    # -------------------------
    # DETECT CONFLICTS
    # -------------------------
    def detect_conflicts(self):
        conflicts = []

        kernels = [f for f in self.active_modules if "kernel" in f]
        swarms = [f for f in self.active_modules if "swarm" in f]

        if len(kernels) > 1:
            conflicts.append(f"Multiple kernels detected: {kernels}")

        if len(swarms) > 3:
            conflicts.append(f"Swarm overload: {len(swarms)} active")

        self.conflicts = conflicts

        return conflicts

    # -------------------------
    # BUILD SELF MODEL
    # -------------------------
    def build_model(self):
        return {
            "tick": self.tick,
            "modules": self.active_modules,
            "conflicts": self.conflicts,
            "health": "stable" if not self.conflicts else "unstable"
        }

    # -------------------------
    # SAVE MODEL
    # -------------------------
    def save(self, model):
        with open(STATE_FILE, "w") as f:
            json.dump(model, f, indent=2)

    # -------------------------
    # EXECUTION CONTROL (SAFE MODE)
    # -------------------------
    def suggest_actions(self):
        actions = []

        kernels = [f for f in self.active_modules if "kernel" in f]

        if len(kernels) > 1:
            actions.append("STOP duplicate kernels (keep latest only)")

        if len(self.conflicts) > 0:
            actions.append("Reduce swarm instances")

        return actions

    # -------------------------
    # STEP LOOP
    # -------------------------
    def step(self):
        self.tick += 1

        self.scan_files()
        self.detect_conflicts()

        model = self.build_model()
        self.save(model)

        actions = self.suggest_actions()

        print("\n[V13 SELF-MODEL]")
        print("tick:", self.tick)
        print("modules:", len(self.active_modules))
        print("conflicts:", len(self.conflicts))

        if actions:
            print("ACTIONS:")
            for a in actions:
                print(" -", a)
        else:
            print("system: stable")

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V13] SELF-MODEL LAYER ONLINE")

        while True:
            self.step()
            time.sleep(3)


# -------------------------
# BOOT
# -------------------------
if __name__ == "__main__":
    try:
        OmegaSelfModelV13().run()
    except KeyboardInterrupt:
        print("\n[V13] shutdown clean")
