import os
import time
import json
import subprocess
from collections import defaultdict, deque


# =========================================================
# 🧠 SYSTEM HEALTH ENGINE
# =========================================================
class SystemHealth:
    def __init__(self):
        self.score = 100
        self.failures = 0

    def degrade(self, amount):
        self.score -= amount
        self.failures += 1
        self.score = max(0, self.score)

    def status(self):
        if self.score > 80:
            return "STABLE"
        if self.score > 50:
            return "DEGRADED"
        if self.score > 20:
            return "CRITICAL"
        return "EMERGENCY"


# =========================================================
# 🧠 BOOT STAGES (LINUX SIMULATION)
# =========================================================
BOOT_STAGES = [
    "INIT",
    "KERNEL",
    "SYSTEMD",
    "USERSPACE",
    "RUNNING"
]


# =========================================================
# 🧠 DAG ENGINE
# =========================================================
class DAGV8:
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
# 🧠 OMEGA OS BRAIN v8
# =========================================================
class OmegaOSBrainV8:
    def __init__(self):
        self.base = os.path.expanduser("~/Omega/OmegaV6")

        self.dag = DAGV8()
        self.health = SystemHealth()

        self.processes = {}
        self.boot_stage = "INIT"

        self.cpu_pressure = 0.0
        self.mem_pressure = 0.0

    # =====================================================
    # 🧠 DISCOVERY (LINUX STYLE SERVICE SCAN)
    # =====================================================
    def discover(self):
        services = []

        for f in os.listdir(self.base):
            if not f.endswith(".py"):
                continue

            services.append({
                "name": f,
                "exec": f,
                "requires": [],
                "cpu": 0.5,
                "mem": 128,
                "critical": "kernel" in f or "runtime" in f
            })

        return services

    # =====================================================
    # 🧠 BOOT SIMULATION PIPELINE
    # =====================================================
    def boot(self):
        print("\n🧠 OMEGA OS BRAIN v8 - LINUX BOOT SIMULATION\n")

        services = self.discover()

        order = self.dag.resolve(services)

        # -----------------------------
        # BOOT PHASE 1: INIT
        # -----------------------------
        self.boot_stage = "INIT"
        print("🔵 INIT phase starting...")
        time.sleep(0.5)

        # -----------------------------
        # BOOT PHASE 2: KERNEL
        # -----------------------------
        self.boot_stage = "KERNEL"
        print("🟡 KERNEL loading core services...")

        # -----------------------------
        # BOOT PHASE 3: SYSTEMD
        # -----------------------------
        self.boot_stage = "SYSTEMD"
        print("🟠 SYSTEMD service manager active")

        # -----------------------------
        # BOOT PHASE 4: USERSPACE
        # -----------------------------
        self.boot_stage = "USERSPACE"

        print("\n🧩 BOOT ORDER:")
        for o in order:
            print(" →", o)

        self.launch(services, order)

        # -----------------------------
        # BOOT COMPLETE
        # -----------------------------
        self.boot_stage = "RUNNING"
        print("\n🟢 SYSTEM FULLY BOOTED")

        self.monitor()

    # =====================================================
    # 🧠 RESOURCE SIMULATION (CPU / MEM PRESSURE)
    # =====================================================
    def simulate_load(self, svc):
        self.cpu_pressure += svc["cpu"]
        self.mem_pressure += svc["mem"] / 1024

        # OOM SIMULATION
        if self.mem_pressure > 2.5:
            self.health.degrade(15)
            print("🔥 OOM EVENT: memory pressure high")

        # CPU THROTTLING SIMULATION
        if self.cpu_pressure > 3.0:
            self.health.degrade(10)
            print("⚠️ CPU THROTTLING ACTIVE")

    # =====================================================
    # 🧠 LAUNCH SERVICES
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
                    "svc": svc
                }

                self.simulate_load(svc)

                print(f"🚀 STARTED: {name} PID={p.pid}")

            except Exception:
                self.health.degrade(5)
                print(f"❌ FAILED: {name}")

    # =====================================================
    # 🧠 RUNTIME MONITOR (LINUX KERNEL STYLE)
    # =====================================================
    def monitor(self):
        while True:
            time.sleep(3)

            print(f"\n🧠 SYSTEM STATUS: {self.health.status()} ({self.health.score}/100)")
            print(f"📊 BOOT STAGE: {self.boot_stage}")
            print(f"⚙️ CPU LOAD: {self.cpu_pressure:.2f}")
            print(f"💾 MEM LOAD: {self.mem_pressure:.2f}")

            for name, data in list(self.processes.items()):
                proc = data["proc"]

                if proc.poll() is not None:
                    print(f"⚠️ SERVICE DEAD: {name}")
                    self.health.degrade(10)


# =========================================================
# 🧠 BOOT ENTRYPOINT
# =========================================================
if __name__ == "__main__":
    OmegaOSBrainV8().boot()
