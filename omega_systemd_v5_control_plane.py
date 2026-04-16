#!/usr/bin/env python3

import os
import time
import subprocess
import json
from collections import defaultdict

MAX_MODULES = 25
RESTART_LIMIT = 2
COOLDOWN = 2

STATE_FILE = os.path.expanduser("~/Omega/omega_control_plane_state.json")


class ControlPlaneV5:
    def __init__(self):
        self.processes = {}
        self.restart_count = defaultdict(int)
        self.load_state()

    # ---------------- STATE ----------------
    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                self.state = json.load(f)
        else:
            self.state = {"active": {}, "dead": {}}

    def save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    # ---------------- LAUNCH ----------------
    def launch(self, module, role="service"):
        if module in self.processes:
            return

        print(f"🚀 LAUNCH [{role}]: {module}")

        try:
            p = subprocess.Popen(
                ["python", os.path.expanduser(f"~/Omega/{module}")],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            self.processes[module] = {
                "pid": p.pid,
                "role": role,
                "time": time.time()
            }

            self.state["active"][module] = p.pid
            self.save_state()

        except Exception as e:
            print(f"❌ FAIL: {module} -> {e}")

    # ---------------- MONITOR ----------------
    def is_alive(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except:
            return False

    def monitor(self):
        while True:
            time.sleep(COOLDOWN)

            dead = []

            for module, meta in list(self.processes.items()):
                pid = meta["pid"]

                if not self.is_alive(pid):
                    dead.append(module)

            for module in dead:
                print(f"\n⚠️ DEAD: {module}")

                self.state["dead"][module] = self.state["dead"].get(module, 0) + 1

                # restart policy
                if self.state["dead"][module] <= RESTART_LIMIT:
                    print(f"🔁 RESTARTING: {module}")
                    self.launch(module, self.processes[module]["role"])
                else:
                    print(f"🛑 KILLED (limit reached): {module}")

                    if module in self.processes:
                        del self.processes[module]

                self.save_state()


    # ---------------- BOOT STRAP ----------------
    def boot(self):
        print("\n🧠 OMEGA SYSTEMD v5 CONTROL PLANE\n")

        modules = self.discover_modules()

        print(f"📦 Modules discovered: {len(modules)}")
        print(f"🎯 MAX ACTIVE: {MAX_MODULES}\n")

        selected = modules[:MAX_MODULES]

        for i, m in enumerate(selected):
            role = self.assign_role(m)
            self.launch(m, role)
            time.sleep(0.2)

        print("\n🟢 CONTROL PLANE ONLINE\n")
        self.monitor()

    # ---------------- DISCOVERY ----------------
    def discover_modules(self):
        base = os.path.expanduser("~/Omega")
        files = []

        for f in os.listdir(base):
            if f.endswith(".py") and "omega" in f.lower():
                files.append(f)

        return sorted(files)

    # ---------------- ROLE ENGINE ----------------
    def assign_role(self, module):
        if "kernel" in module:
            return "kernel"
        if "brain" in module:
            return "brain"
        if "swarm" in module:
            return "swarm"
        if "mesh" in module:
            return "mesh"
        return "service"


if __name__ == "__main__":
    ControlPlaneV5().boot()
