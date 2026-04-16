import os
import time
import json
import subprocess
from collections import defaultdict, deque

LOG = "[OMEGA SYSTEMD v1]"
MANIFEST = "omega_manifest.json"


def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG} {msg}")


def load_manifest():
    if not os.path.exists(MANIFEST):
        log("❌ Missing manifest")
        return None

    with open(MANIFEST, "r") as f:
        return json.load(f)


STATE_PENDING = "PENDING"
STATE_ACTIVE = "ACTIVE"
STATE_FAILED = "FAILED"
STATE_ISOLATED = "ISOLATED"


class DAG:
    def __init__(self):
        self.graph = defaultdict(list)
        self.indegree = defaultdict(int)

    def add(self, service, deps):
        if service not in self.indegree:
            self.indegree[service] = 0

        for d in deps:
            self.graph[d].append(service)
            self.indegree[service] += 1
            if d not in self.indegree:
                self.indegree[d] = 0

    def resolve_order(self):
        q = deque([n for n in self.indegree if self.indegree[n] == 0])
        order = []

        while q:
            node = q.popleft()
            order.append(node)

            for neigh in self.graph[node]:
                self.indegree[neigh] -= 1
                if self.indegree[neigh] == 0:
                    q.append(neigh)

        return order


class Service:
    def __init__(self, name):
        self.name = name
        self.proc = None
        self.state = STATE_PENDING
        self.restarts = 0

    def launch(self):
        if not os.path.exists(self.name):
            self.state = STATE_FAILED
            log(f"⚠️ Missing: {self.name}")
            return False

        log(f"🚀 START → {self.name}")

        self.proc = subprocess.Popen(
            ["python", self.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.state = STATE_ACTIVE
        return True

    def dead(self):
        return self.proc and self.proc.poll() is not None


class OmegaSystemD:
    def __init__(self, manifest):
        self.raw = manifest.get("services", {})
        self.services = {}
        self.dag = DAG()
        self.isolated = set()

        self._build_services()
        self._build_dag()

    def _build_services(self):
        for s in self.raw:
            self.services[s] = Service(s)

    def _build_dag(self):
        if isinstance(self.raw, dict):
            for s, deps in self.raw.items():
                self.dag.add(s, deps)
        else:
            prev = None
            for s in self.raw:
                deps = [prev] if prev else []
                self.dag.add(s, deps)
                prev = s

    def boot(self):
        log("🧠 BOOT START")

        order = self.dag.resolve_order()
        log(f"📦 BOOT ORDER: {order}")

        for s in order:
            self.start(s)

        log("🟢 BOOT COMPLETE")
        self.monitor()

    def start(self, s):
        if s in self.isolated:
            return
        self.services[s].launch()

    def isolate(self, s):
        self.isolated.add(s)
        log(f"🧊 ISOLATED → {s}")

    def restart(self, s):
        svc = self.services[s]

        if svc.restarts >= 3:
            self.isolate(s)
            return

        log(f"🔁 RESTART → {s}")

        try:
            svc.proc.terminate()
        except:
            pass

        time.sleep(1)

        svc.restarts += 1
        svc.launch()

    def monitor(self):
        while True:
            time.sleep(2)

            for s, svc in self.services.items():
                if s in self.isolated:
                    continue

                if svc.dead():
                    log(f"💀 DEAD → {s}")
                    self.restart(s)


if __name__ == "__main__":
    manifest = load_manifest()
    if not manifest:
        exit(1)

    OmegaSystemD(manifest).boot()
