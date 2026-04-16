import json
import subprocess
import time
import os
from collections import defaultdict, deque

class OmegaOSBrainV8:

    def __init__(self, manifest_path="omega_manifest.json"):
        self.manifest_path = manifest_path

        self.running = {}
        self.failed = set()

        # HARD LIMITS (this stops your chaos)
        self.limits = {
            "service": 12,
            "tool": 20,
            "kernel": 1,
        }

    # -------------------------------
    # CLASSIFICATION ENGINE
    # -------------------------------
    def classify(self, modules):
        classified = {
            "service": [],
            "library": [],
            "tool": [],
            "data": []
        }

        for m in modules:
            if m.get("type") == "service":
                classified["service"].append(m)
            elif m.get("type") == "library":
                classified["library"].append(m)
            elif m.get("type") == "tool":
                classified["tool"].append(m)
            else:
                classified["data"].append(m)

        return classified

    # -------------------------------
    # NORMALIZE SERVICES (FIXED CORE)
    # -------------------------------
    def normalize_services(self, discovered, manifest):
        discovered_set = set(discovered)

        normalized = []
        degraded = []
        missing_core = []

        for svc in manifest:

            name = svc.get("name", "")
            exec_file = svc.get("exec", "")

            if exec_file in discovered_set:
                normalized.append(svc)
            else:
                if name in ["kernel", "runtime"]:
                    missing_core.append(svc)
                    print(f"❌ CRITICAL MISSING CORE: {exec_file}")
                else:
                    degraded.append(svc)
                    print(f"⚠️ DEGRADED SERVICE: {exec_file}")

        return normalized, degraded, missing_core

    # -------------------------------
    # DAG RESOLVER (BOOT ORDER)
    # -------------------------------
    def resolve_dag(self, services):
        graph = defaultdict(list)
        indegree = defaultdict(int)

        for s in services:
            name = s["name"]
            deps = s.get("depends", [])

            for d in deps:
                graph[d].append(name)
                indegree[name] += 1

            if name not in indegree:
                indegree[name] = indegree[name]

        queue = deque([n for n in indegree if indegree[n] == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for neigh in graph[node]:
                indegree[neigh] -= 1
                if indegree[neigh] == 0:
                    queue.append(neigh)

        return order

    # -------------------------------
    # EXECUTION GUARD (ANTI-CHAOS)
    # -------------------------------
    def can_launch(self, svc_type):
        return len([x for x in self.running.values() if x["type"] == svc_type]) < self.limits.get(svc_type, 5)

    # -------------------------------
    # LAUNCH PROCESS (ONLY KERNEL USES THIS)
    # -------------------------------
    def launch(self, service):
        if not self.can_launch(service["type"]):
            print(f"🚫 LIMIT BLOCKED: {service['name']}")
            return None

        try:
            proc = subprocess.Popen(["python", service["exec"]])

            self.running[service["name"]] = {
                "pid": proc.pid,
                "type": service["type"],
                "restarts": 0
            }

            print(f"🚀 STARTED: {service['name']} PID={proc.pid}")
            return proc

        except Exception as e:
            print(f"❌ LAUNCH FAILED: {service['name']} -> {e}")
            self.failed.add(service["name"])
            return None

    # -------------------------------
    # BOOT SEQUENCE
    # -------------------------------
    def boot(self):
        print("\n🧠 OMEGA OS BRAIN v8 (CONTROL PLANE)\n")

        if not os.path.exists(self.manifest_path):
            print("❌ Missing manifest file")
            return

        with open(self.manifest_path, "r") as f:
            manifest = json.load(f)["services"]

        discovered = [m["exec"] for m in manifest]

        service_manifest, degraded, missing_core = self.normalize_services(
            discovered,
            manifest
        )

        if missing_core:
            print("\n🛑 BOOT ABORTED: critical core missing")
            return

        order = self.resolve_dag(service_manifest)

        print("\n🧩 BOOT ORDER:")
        for o in order:
            print(" →", o)

        # launch services in order
        for name in order:
            svc = next((s for s in service_manifest if s["name"] == name), None)
            if svc:
                self.launch(svc)

        self.monitor()

    # -------------------------------
    # WATCHDOG (NO SPAM RESTARTS)
    # -------------------------------
    def monitor(self):
        print("\n🧠 WATCHDOG ACTIVE\n")

        while True:
            time.sleep(5)

            for name, info in list(self.running.items()):
                pid = info["pid"]

                if not self._is_alive(pid):
                    print(f"⚠️ DEAD: {name} PID={pid}")

                    if info["restarts"] < 2:
                        print(f"♻️ RESTARTING: {name}")
                        info["restarts"] += 1
                    else:
                        print(f"🛑 MAX RESTARTS REACHED: {name}")
                        del self.running[name]

    # -------------------------------
    # PROCESS CHECK
    # -------------------------------
    def _is_alive(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except:
            return False


if __name__ == "__main__":
    OmegaOSBrainV8().boot()
