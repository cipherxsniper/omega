import os
import json
import subprocess
import time


class OmegaServiceClassifierV5:
    """
    NOT ALL CODE IS A SERVICE
    """

    def classify(self, name: str) -> str:
        n = name.lower()

        if "kernel" in n:
            return "kernel"

        if any(x in n for x in [
            "orchestrator", "engine", "brain",
            "swarm", "runtime", "supervisor",
            "daemon", "process"
        ]):
            return "service"

        if n.endswith(".json") or n.endswith(".log"):
            return "data"

        if any(x in n for x in [
            "graph", "memory", "parser",
            "resolver", "compiler", "patch",
            "classifier", "registry"
        ]):
            return "library"

        return "tool"


class OmegaDAGEngineV5:
    def resolve(self, services):
        from collections import defaultdict, deque

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


class OmegaOSBrainV5:
    def __init__(self):
        self.base = os.path.expanduser("~/Omega/OmegaV6")
        self.processes = {}

        self.classifier = OmegaServiceClassifierV5()
        self.dag = OmegaDAGEngineV5()

    # =========================================================
    # 🧠 SERVICE RECONCILIATION (UPGRADED v5 CORE LOGIC)
    # =========================================================
    def normalize_services(self, discovered, manifest):
        discovered_set = set(discovered)

        normalized = []
        degraded = []
        missing_core = []

        for svc in manifest:
            exec_name = svc["exec"]

            if exec_name in discovered_set:
                normalized.append(svc)
            else:
                # 🔥 CLASSIFY SEVERITY
                if svc["name"] in ["runtime", "kernel"]:
                    missing_core.append(svc)
                    print(f"❌ CRITICAL MISSING CORE: {exec_name}")
                else:
                    degraded.append(svc)
                    print(f"⚠️ DEGRADED SERVICE (skipped): {exec_name}")

        return normalized, degraded, missing_core

    # =========================================================
    # 🧠 DISCOVERY LAYER
    # =========================================================
    def discover(self):
        manifest = {
            "kernel": [],
            "service": [],
            "library": [],
            "tool": [],
            "data": []
        }

        for f in os.listdir(self.base):
            if not (f.endswith(".py") or f.endswith(".json") or f.endswith(".log")):
                continue

            category = self.classifier.classify(f)
            manifest[category].append(f)

        return manifest

    # =========================================================
    # 🧠 BOOT SEQUENCE (FIXED SAFE FLOW)
    # =========================================================
    def boot(self):
        print("\n🧠 OMEGA OS BRAIN v5 (SYSTEMD SAFETY GATE)\n")

        manifest = self.discover()

        print("📦 DISCOVERY COMPLETE")
        for k, v in manifest.items():
            print(f"   {k}: {len(v)}")

        # load systemd-style manifest
        with open("omega_service_manifest_v3.json") as f:
            service_manifest = json.load(f)["services"]

        # =====================================================
        # 🔥 PATCH 2 IMPLEMENTATION (REAL FIXED FLOW)
        # =====================================================

        service_manifest, degraded, missing_core = self.normalize_services(
            manifest["service"],
            service_manifest
        )

        # 🛑 SAFETY GATE (CRITICAL CORE PROTECTION)
        if missing_core:
            print("\n🛑 BOOT ABORTED: critical core missing services detected")
            return

        order = self.dag.resolve(service_manifest)

        print("\n🧩 BOOT ORDER (SERVICES ONLY):")
        for o in order:
            print(" →", o)

        self.launch(service_manifest, order)
        self.monitor()

    # =========================================================
    # 🧠 LAUNCH SYSTEM
    # =========================================================
    def launch(self, services, order):
        for name in order:
            svc = next((s for s in services if s["name"] == name), None)
            if not svc:
                continue

            path = os.path.join(self.base, svc["exec"])

            if not os.path.exists(path):
                print(f"❌ MISSING FILE: {svc['exec']}")
                continue

            p = subprocess.Popen(["python", path])
            self.processes[name] = p

            print(f"🚀 STARTED: {name} PID={p.pid}")

    # =========================================================
    # 🧠 MONITOR LOOP
    # =========================================================
    def monitor(self):
        while True:
            time.sleep(5)

            for name, proc in list(self.processes.items()):
                if proc.poll() is not None:
                    print(f"⚠️ SERVICE DEAD: {name}")
                    print(f"♻️ RESTARTING: {name}")

                    self.processes.pop(name, None)


if __name__ == "__main__":
    OmegaOSBrainV5().boot()
