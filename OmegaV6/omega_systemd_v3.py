import time
import json
import subprocess
import os
from collections import defaultdict

# ---------------------------
# STATES
# ---------------------------

STARTING = "STARTING"
ACTIVE = "ACTIVE"
DEGRADED = "DEGRADED"
FAILED = "FAILED"
BLOCKED = "BLOCKED"
DEAD = "DEAD"

LOG_FILE = "omega_journal_v3.log"

# ---------------------------
# JOURNALD BUS
# ---------------------------

class Journal:
    def log(self, level, service, msg):
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "level": level,
            "service": service,
            "msg": msg
        }
        print(f"[{level}] {service} → {msg}")
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")

# ---------------------------
# HEARTBEAT REGISTRY
# ---------------------------

class HeartbeatBus:
    def __init__(self):
        self.last_beat = {}

    def beat(self, service):
        self.last_beat[service] = time.time()

    def check(self, service, timeout=6):
        last = self.last_beat.get(service)
        if not last:
            return False
        return (time.time() - last) < timeout

# ---------------------------
# DEPENDENCY ENGINE (DAG)
# ---------------------------

class DependencyGraph:
    def __init__(self, services):
        self.graph = defaultdict(list)
        self.services = services
        self.build()

    def build(self):
        # simple ordered DAG (upgradeable later to real resolver)
        for i in range(len(self.services) - 1):
            self.graph[self.services[i]].append(self.services[i + 1])

    def resolve(self):
        # returns ordered list (topological-lite)
        visited = set()
        order = []

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for n in self.graph.get(node, []):
                dfs(n)
            order.append(node)

        for s in self.services:
            dfs(s)

        return list(reversed(order))

# ---------------------------
# SERVICE CONTROL BLOCK
# ---------------------------

class Service:
    def __init__(self, name):
        self.name = name
        self.proc = None
        self.state = STARTING
        self.restarts = 0
        self.last_heartbeat = time.time()

# ---------------------------
# KERNEL v3
# ---------------------------

class OmegaSystemD3:

    def __init__(self, manifest):
        self.journal = Journal()
        self.heartbeat = HeartbeatBus()

        self.services = {
            s: Service(s)
            for s in manifest.get("services", [])
        }

        self.dep = DependencyGraph(list(self.services.keys()))
        self.blocked = set()

    # ---------------------------
    # LAUNCH SERVICE
    # ---------------------------

    def start(self, name):
        svc = self.services[name]

        if name in self.blocked:
            self.journal.log("BLOCK", name, "service blocked")
            return

        self.journal.log("INFO", name, "starting")
        svc.state = STARTING

        try:
            svc.proc = subprocess.Popen(
                ["python", name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            svc.state = ACTIVE
            self.heartbeat.beat(name)

        except Exception as e:
            svc.state = FAILED
            self.journal.log("ERROR", name, str(e))

    # ---------------------------
    # RESTART POLICY
    # ---------------------------

    def restart(self, name):
        svc = self.services[name]

        if svc.restarts >= 3:
            svc.state = BLOCKED
            self.blocked.add(name)
            self.journal.log("BLOCK", name, "restart limit reached")
            return

        self.journal.log("WARN", name, "restarting")
        svc.restarts += 1

        self.start(name)

    # ---------------------------
    # HEARTBEAT WATCHDOG
    # ---------------------------

    def watchdog(self):
        for name, svc in self.services.items():

            if svc.state == BLOCKED:
                continue

            alive = svc.proc and svc.proc.poll() is None
            heartbeat_ok = self.heartbeat.check(name)

            if not alive:
                svc.state = FAILED
                self.journal.log("WARN", name, "process dead")
                self.restart(name)
                continue

            if not heartbeat_ok:
                svc.state = DEGRADED
                self.journal.log("WARN", name, "missing heartbeat")

    # ---------------------------
    # BOOT SEQUENCE (DAG ORDER)
    # ---------------------------

    def boot(self):
        order = self.dep.resolve()

        self.journal.log("INFO", "SYSTEM", f"boot order: {order}")

        for s in order:
            self.start(s)

        self.journal.log("INFO", "SYSTEM", "BOOT COMPLETE")

        self.loop()

    # ---------------------------
    # MAIN LOOP
    # ---------------------------

    def loop(self):
        while True:
            time.sleep(3)
            self.watchdog()

            # simulate heartbeat updates from running services
            for name in self.services:
                svc = self.services[name]
                if svc.state == ACTIVE:
                    self.heartbeat.beat(name)


# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":

    if not os.path.exists("omega_manifest.json"):
        print("❌ Missing manifest")
        exit(1)

    manifest = json.load(open("omega_manifest.json"))

    kernel = OmegaSystemD3(manifest)
    kernel.boot()
