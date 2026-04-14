import os
import time
import subprocess

from omega_service_whitelist import filter_core
from omega_service_priority import get_priority, PRIORITY_ORDER

LOG_PREFIX = "[OMEGA V3 KERNEL]"

def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG_PREFIX} {msg}")

def discover_services():
    return [f for f in os.listdir(".") if f.endswith(".py") and f != os.path.basename(__file__)]

class OmegaKernelV3:

    def __init__(self):
        all_services = discover_services()

        # 🧠 FILTER CORE SERVICES ONLY
        self.services = filter_core(all_services)

        # ⚡ PRIORITY ORDERING
        self.services.sort(key=lambda s: PRIORITY_ORDER.get(get_priority(s), 2))

        self.processes = {}
        self.dead_counts = {}
        self.lazy_services = set()

    # ---------------------------
    # START SERVICE
    # ---------------------------
    def start(self, service):

        # 🚨 MAX LIMIT SAFETY
        if len(self.processes) >= 10:
            log("⚠️ MAX PROCESS LIMIT REACHED")
            return

        # 🧠 LAZY SYSTEM
        if get_priority(service) == "LAZY":
            self.lazy_services.add(service)
            log(f"⏳ LAZY DEFERRED → {service}")
            return

        # ❌ BLOCK INVALID FILES
        if not os.path.exists(service):
            log(f"⚠️ MISSING → {service}")
            return

        # 🧠 START PROCESS
        log(f"🚀 START → {service}")
        # 🧠 SERVICE TYPE CHECK
        try:
            with open(service, "r") as f:
                content = f.read()
                if "while True" not in content:
                    log(f"⚠️ JOB MODE (not daemon) → {service}")


        proc = subprocess.Popen(
            ["python", service],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # ⚡ POST START VALIDATION (CRITICAL FIX)
        time.sleep(0.2)

        if proc.poll() is not None:
            log(f"❌ FAILED START → {service}")
            return

        self.processes[service] = proc

    # ---------------------------
    # LAZY SPAWN
    # ---------------------------
    def spawn_lazy(self, service):
        if service in self.lazy_services:
            log(f"⚡ SPAWN LAZY → {service}")
            self.lazy_services.remove(service)
            self.start(service)

    # ---------------------------
    # MONITOR LOOP (FIXED)
    # ---------------------------
    def monitor(self):
        while True:
            time.sleep(2)

            for service, proc in list(self.processes.items()):

                if proc.poll() is not None:

                    self.dead_counts[service] = self.dead_counts.get(service, 0) + 1

                    log(f"💀 DEAD → {service} (count={self.dead_counts[service]})")

                    # 🧊 ISOLATION RULE
                    if self.dead_counts[service] > 3:
                        log(f"🧊 ISOLATED → {service}")
                        del self.processes[service]
                        continue

                    # 🔁 RESTART RULE
                    log(f"🔁 RESTART → {service}")
                    self.start(service)

    # ---------------------------
    # BOOT SEQUENCE
    # ---------------------------
    def boot(self):
        log("🧠 BOOT START")
        log(f"📦 SERVICES: {self.services}")

        for s in self.services:
            self.start(s)

        log("🟢 BOOT COMPLETE")
        self.monitor()


if __name__ == "__main__":
    OmegaKernelV3().boot()
