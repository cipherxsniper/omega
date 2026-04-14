import os
import time
import subprocess
from collections import defaultdict, deque

LOG = "[OMEGA SYSTEMD v5 OS]"

# ----------------------------
# LOGGING
# ----------------------------
def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG} {msg}")

# ----------------------------
# SERVICE DISCOVERY
# ----------------------------
def discover_services():
    return [f for f in os.listdir(".") if f.endswith(".py")]

# ----------------------------
# DAG BUILDER
# ----------------------------
def build_dag(services):
    graph = defaultdict(list)

    for s in services:
        if "kernel" in s:
            graph[s].append("execution")
        if "brain" in s:
            graph[s].append("memory")

    return graph

def topo_sort(nodes, graph):
    indeg = defaultdict(int)

    for u in graph:
        for v in graph[u]:
            indeg[v] += 1

    q = deque([n for n in nodes if indeg[n] == 0])
    order = []

    while q:
        n = q.popleft()
        order.append(n)

        for v in graph.get(n, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    return order if order else nodes

# ----------------------------
# CGROUP SIMULATION
# ----------------------------
class CGroups:

    def __init__(self):
        self.cpu = {}
        self.mem = {}

    def assign(self, service):
        self.cpu[service] = 20   # 20% CPU budget
        self.mem[service] = 128  # MB simulated

    def throttle(self, service):
        log(f"🐢 THROTTLE → {service}")

# ----------------------------
# AI CRASH ANALYZER
# ----------------------------
class CrashAI:

    def analyze(self, service, proc):

        if proc.returncode is None:
            return "UNKNOWN"

        if proc.returncode == 0:
            return "EXIT_OK"

        if proc.returncode == 1:
            return "EXIT_IMMEDIATE"

        if proc.returncode == 2:
            return "IMPORT_ERROR"

        if proc.returncode < 0:
            return "CRASH_LOOP"

        return "UNKNOWN"

# ----------------------------
# KERNEL CORE
# ----------------------------
class OmegaSystemD5Kernel:

    def __init__(self):
        self.services = discover_services()
        self.graph = build_dag(self.services)
        self.order = topo_sort(self.services, self.graph)

        self.processes = {}
        self.cgroups = CGroups()
        self.ai = CrashAI()

        self.restarts = {}

    # ------------------------
    # START SERVICE
    # ------------------------
    def start(self, service):

        if service in self.processes:
            return

        self.cgroups.assign(service)

        log(f"🚀 START → {service}")

        proc = subprocess.Popen(
            ["python", service],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.processes[service] = proc
        self.restarts.setdefault(service, 0)

    # ------------------------
    # RESTART POLICY
    # ------------------------
    def restart(self, service, reason):

        self.restarts[service] += 1

        if self.restarts[service] > 3:
            log(f"🧊 BLOCKED → {service}")
            return

        log(f"🔁 RESTART → {service} ({reason})")
        self.start(service)

    # ------------------------
    # MONITOR LOOP
    # ------------------------
    def monitor(self):

        while True:
            time.sleep(2)

            for service, proc in list(self.processes.items()):

                if proc.poll() is not None:

                    reason = self.ai.analyze(service, proc)

                    log(f"💀 DEAD → {service} | reason={reason}")

                    if reason == "IMPORT_ERROR":
                        log(f"🧠 FIX SUGGESTED → check imports in {service}")

                    if reason in ["EXIT_IMMEDIATE", "UNKNOWN"]:
                        self.restart(service, reason)

                    if reason == "CRASH_LOOP":
                        log(f"🧊 ISOLATED → {service}")
                        continue

    # ------------------------
    # BOOT SEQUENCE
    # ------------------------
    def boot(self):

        log("🧠 BOOT START")
        log(f"📦 SERVICES FOUND: {len(self.services)}")

        for s in self.order:
            self.start(s)

        log("🟢 BOOT COMPLETE")

        self.monitor()

# ----------------------------
# ENTRY
# ----------------------------
if __name__ == "__main__":
    OmegaSystemD5Kernel().boot()
