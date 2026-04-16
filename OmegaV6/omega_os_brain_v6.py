import os
import time
import json
import subprocess
from collections import defaultdict, deque


# =========================================================
# 🧠 SYSTEMD UNIT PARSER
# =========================================================
class UnitParserV6:
    """
    Parses simplified systemd-style .service files
    """

    def parse(self, service):
        # fallback defaults if metadata missing
        return {
            "name": service.get("name"),
            "exec": service.get("exec"),
            "requires": service.get("requires", []),
            "restart": service.get("restart", "on-failure"),
            "watchdog": service.get("watchdog", 0),
            "critical": service.get("critical", False),
        }


# =========================================================
# 🧠 DAG ENGINE
# =========================================================
class DAGV6:
    def resolve(self, services):
        graph = defaultdict(list)
        indeg = defaultdict(int)

        names = {s["name"] for s in services}

        for s in services:
            indeg.setdefault(s["name"], 0)

            for dep in s.get("requires", []):
                if dep in names:
                    graph[dep].append(s["name"])
                    indeg[s["name"]] += 1

        q = deque([n for n in names if indeg[n] == 0])
        order = []

        while q:
            node = q.popleft()
            order.append(node)

            for nxt in graph[node]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    q.append(nxt)

        return order


# =========================================================
# 🧠 OMEGA OS BRAIN v6 KERNEL
# =========================================================
class OmegaOSBrainV6:
    def __init__(self):
        self.base = os.path.expanduser("~/Omega/OmegaV6")

        self.parser = UnitParserV6()
        self.dag = DAGV6()

        self.processes = {}
        self.last_heartbeat = {}
        self.state = "INIT"

    # =====================================================
    # 🧠 DISCOVERY LAYER
    # =====================================================
    def discover(self):
        """
        Converts raw filesystem into service units
        """
        units = []

        for f in os.listdir(self.base):
            if not f.endswith(".py"):
                continue

            # simplistic service inference (v6 kernel behavior)
            unit = {
                "name": f,
                "exec": f,
                "requires": [],
                "restart": "on-failure",
                "watchdog": 0,
                "critical": "kernel" in f or "runtime" in f
            }

            units.append(self.parser.parse(unit))

        return units

    # =====================================================
    # 🧠 SERVICE NORMALIZATION
    # =====================================================
    def normalize(self, services):
        valid = []
        degraded = []
        missing_core = []

        discovered = set(os.listdir(self.base))

        for s in services:
            if s["exec"] in discovered:
                valid.append(s)
            else:
                if s["critical"]:
                    missing_core.append(s)
                    print(f"❌ CRITICAL MISSING: {s['exec']}")
                else:
                    degraded.append(s)
                    print(f"⚠️ DEGRADED SERVICE: {s['exec']}")

        return valid, degraded, missing_core

    # =====================================================
    # 🧠 BOOT KERNEL
    # =====================================================
    def boot(self):
        print("\n🧠 OMEGA OS BRAIN v6 SYSTEMD KERNEL\n")

        services = self.discover()
        services, degraded, missing_core = self.normalize(services)

        if missing_core:
            self.state = "EMERGENCY"
            print("\n🛑 EMERGENCY BOOT ABORTED: missing core services")
            return

        order = self.dag.resolve(services)

        print("\n🧩 BOOT ORDER:")
        for o in order:
            print(" →", o)

        self.launch(services, order)
        self.state = "RUNNING"
        self.monitor()

    # =====================================================
    # 🧠 LAUNCH SYSTEM
    # =====================================================
    def launch(self, services, order):
        for name in order:
            svc = next((s for s in services if s["name"] == name), None)
            if not svc:
                continue

            path = os.path.join(self.base, svc["exec"])

            try:
                p = subprocess.Popen(["python", path])
                self.processes[name] = {
                    "proc": p,
                    "restart": svc["restart"],
                    "watchdog": svc["watchdog"]
                }

                self.last_heartbeat[name] = time.time()

                print(f"🚀 STARTED: {name} PID={p.pid}")

            except Exception as e:
                print(f"❌ LAUNCH FAILED: {name} -> {e}")

    # =====================================================
    # 🧠 WATCHDOG + FAILURE ENGINE
    # =====================================================
    def monitor(self):
        while True:
            time.sleep(3)

            for name, data in list(self.processes.items()):
                proc = data["proc"]

                # DEAD PROCESS DETECTION
                if proc.poll() is not None:
                    print(f"⚠️ SERVICE DEAD: {name}")

                    if data["restart"] == "always":
                        print(f"♻️ RESTARTING (always): {name}")
                        self.restart(name, data)

                    elif data["restart"] == "on-failure":
                        print(f"♻️ RESTARTING (on-failure): {name}")
                        self.restart(name, data)

                    else:
                        print(f"🛑 NOT RESTARTED (policy): {name}")

                # WATCHDOG CHECK
                if data["watchdog"] > 0:
                    if time.time() - self.last_heartbeat.get(name, 0) > data["watchdog"]:
                        print(f"⏱ WATCHDOG TIMEOUT: {name}")
                        self.restart(name, data)

    # =====================================================
    # 🧠 RESTART ENGINE
    # =====================================================
    def restart(self, name, data):
        try:
            path = os.path.join(self.base, name)

            p = subprocess.Popen(["python", path])

            self.processes[name]["proc"] = p
            self.last_heartbeat[name] = time.time()

            print(f"🚀 RESTARTED: {name} PID={p.pid}")

        except Exception as e:
            print(f"❌ RESTART FAILED: {name} -> {e}")


# =========================================================
# 🧠 BOOT STRAP
# =========================================================
if __name__ == "__main__":
    OmegaOSBrainV6().boot()
