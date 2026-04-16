import os
import time
import json
import subprocess
from collections import defaultdict, deque


# =========================================================
# 🧠 JOURNALD (LOGGING SYSTEM)
# =========================================================
class JournalD:
    def __init__(self):
        self.logs = []

    def log(self, unit, level, msg):
        entry = {
            "time": time.time(),
            "unit": unit,
            "level": level,
            "msg": msg
        }

        self.logs.append(entry)

        print(f"[{level}] {unit}: {msg}")


# =========================================================
# 🧠 CGROUP SIMULATOR
# =========================================================
class CGroupV7:
    def __init__(self):
        self.limits = {}

    def apply(self, name, cpu=1.0, mem=512):
        self.limits[name] = {
            "cpu": cpu,
            "mem": mem
        }


# =========================================================
# 🧠 SYSTEMD UNIT PARSER (INI STYLE)
# =========================================================
class UnitParserV7:
    def parse(self, raw):
        return {
            "name": raw.get("name"),
            "exec": raw.get("exec"),
            "requires": raw.get("requires", []),

            # systemd behavior
            "restart": raw.get("restart", "on-failure"),
            "watchdog": raw.get("watchdog", 0),

            # cgroup simulation
            "cpu": raw.get("cpu", 1.0),
            "mem": raw.get("mem", 512),

            # critical system flag
            "critical": raw.get("critical", False),
        }


# =========================================================
# 🧠 DAG ENGINE
# =========================================================
class DAGV7:
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
# 🧠 OMEGA OS BRAIN v7 KERNEL
# =========================================================
class OmegaOSBrainV7:
    def __init__(self):
        self.base = os.path.expanduser("~/Omega/OmegaV6")

        self.journal = JournalD()
        self.cgroup = CGroupV7()
        self.parser = UnitParserV7()
        self.dag = DAGV7()

        self.processes = {}
        self.backoff = {}
        self.state = "INIT"

    # =====================================================
    # 🧠 DISCOVERY
    # =====================================================
    def discover(self):
        units = []

        for f in os.listdir(self.base):
            if not f.endswith(".py"):
                continue

            unit = {
                "name": f,
                "exec": f,
                "requires": [],

                # default systemd behavior
                "restart": "on-failure",
                "watchdog": 0,

                # fake cgroup values
                "cpu": 0.8,
                "mem": 256,

                "critical": "kernel" in f or "runtime" in f
            }

            units.append(self.parser.parse(unit))

        return units

    # =====================================================
    # 🧠 NORMALIZER
    # =====================================================
    def normalize(self, services):
        discovered = set(os.listdir(self.base))

        valid, degraded, missing = [], [], []

        for s in services:
            if s["exec"] in discovered:
                valid.append(s)
            else:
                if s["critical"]:
                    missing.append(s)
                    self.journal.log(s["name"], "CRITICAL", "missing service")
                else:
                    degraded.append(s)
                    self.journal.log(s["name"], "WARN", "degraded service")

        return valid, degraded, missing

    # =====================================================
    # 🧠 BOOT
    # =====================================================
    def boot(self):
        self.journal.log("SYSTEM", "INFO", "OMEGA OS BRAIN v7 BOOT")

        services = self.discover()
        services, degraded, missing = self.normalize(services)

        if missing:
            self.state = "EMERGENCY"
            self.journal.log("SYSTEM", "FATAL", "boot aborted - missing core services")
            return

        order = self.dag.resolve(services)

        self.journal.log("SYSTEM", "INFO", f"boot order: {order}")

        self.launch(services, order)
        self.state = "RUNNING"
        self.monitor()

    # =====================================================
    # 🧠 LAUNCHER
    # =====================================================
    def launch(self, services, order):
        for name in order:
            svc = next((s for s in services if s["name"] == name), None)
            if not svc:
                continue

            path = os.path.join(self.base, svc["exec"])

            self.cgroup.apply(name, svc["cpu"], svc["mem"])

            try:
                p = subprocess.Popen(["python", path])

                self.processes[name] = {
                    "proc": p,
                    "svc": svc,
                    "status": "ACTIVE"
                }

                self.backoff[name] = 1

                self.journal.log(name, "START", f"PID={p.pid}")

            except Exception as e:
                self.journal.log(name, "ERROR", str(e))

    # =====================================================
    # 🧠 MONITOR + CGROUP + JOURNAL + BACKOFF
    # =====================================================
    def monitor(self):
        while True:
            time.sleep(3)

            for name, data in list(self.processes.items()):
                proc = data["proc"]
                svc = data["svc"]

                # DEAD PROCESS
                if proc.poll() is not None:
                    self.journal.log(name, "FAIL", "process exited")

                    # BACKOFF STRATEGY (prevents restart storms)
                    wait = self.backoff.get(name, 1)
                    time.sleep(wait)
                    self.backoff[name] = min(wait * 2, 30)

                    if svc["restart"] in ["always", "on-failure"]:
                        self.journal.log(name, "RESTART", f"backoff={wait}")
                        self.restart(name, svc)

                # WATCHDOG
                if svc["watchdog"] > 0:
                    self.journal.log(name, "WATCHDOG", "check alive (simulated)")

    # =====================================================
    # 🧠 RESTART ENGINE
    # =====================================================
    def restart(self, name, svc):
        path = os.path.join(self.base, svc["exec"])

        try:
            p = subprocess.Popen(["python", path])

            self.processes[name]["proc"] = p

            self.journal.log(name, "RESTARTED", f"PID={p.pid}")

        except Exception as e:
            self.journal.log(name, "RESTART_FAIL", str(e))


# =========================================================
# 🧠 BOOT STRAP
# =========================================================
if __name__ == "__main__":
    OmegaOSBrainV7().boot()
