import os
import time
import subprocess
import re
from collections import defaultdict

LOG = "[OMEGA V3 KERNEL]"

# ---------------------------
# LOGGER
# ---------------------------

def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG} {msg}")

# ---------------------------
# DISCOVERY ENGINE
# ---------------------------

def extract_base(name):
    if "_v" in name:
        return name.split("_v")[0]
    return name.replace(".py", "")

def extract_version(name):
    try:
        return int(name.split("_v")[-1].split(".")[0])
    except:
        return 0

def discover_services():
    files = [f for f in os.listdir(".") if f.endswith(".py")]

    grouped = defaultdict(list)

    for f in files:
        base = extract_base(f)
        grouped[base].append(f)

    selected = []

    for base, versions in grouped.items():
        best = max(versions, key=extract_version)
        selected.append(best)

    return selected

# ---------------------------
# DEPENDENCY INFERENCE ENGINE
# ---------------------------

IMPORT_RE = re.compile(r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)')

def infer_dependencies(services):
    deps = {s: [] for s in services}

    for service in services:
        try:
            with open(service, "r") as f:
                lines = f.readlines()

            for line in lines:
                match = IMPORT_RE.match(line)
                if match:
                    module = match.group(1) + ".py"
                    if module in services and module != service:
                        deps[service].append(module)

        except:
            continue

    return deps

# ---------------------------
# DAG RESOLVER
# ---------------------------

def resolve_dag(graph):
    visited = set()
    order = []

    def visit(node):
        if node in visited:
            return
        visited.add(node)

        for dep in graph.get(node, []):
            visit(dep)

        order.append(node)

    for s in graph:
        visit(s)

    return order

# ---------------------------
# LAUNCH GUARD
# ---------------------------

def safe_launch(service):
    if not os.path.exists(service):
        log(f"⚠️ Missing: {service}")
        return None

    log(f"🚀 START → {service}")

    return subprocess.Popen(
        ["python", service],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# ---------------------------
# KERNEL
# ---------------------------

class OmegaSystemD3Kernel:

    def __init__(self):
        self.services = discover_services()
        self.graph = infer_dependencies(self.services)
        self.order = resolve_dag(self.graph)

        self.processes = {}
        self.restarts = defaultdict(int)
        self.disabled = set()

    def boot(self):
        log("🧠 BOOT START")

        log(f"📦 DISCOVERED: {len(self.services)} services")
        log(f"🧬 BOOT ORDER: {self.order}")

        for service in self.order:
            self.start(service)

        log("🟢 BOOT COMPLETE")
        self.monitor()

    def start(self, service):
        if service in self.disabled:
            return

        proc = safe_launch(service)

        if proc:
            self.processes[service] = proc

    def restart(self, service):
        if service in self.disabled:
            return

        if self.restarts[service] > 2:
            log(f"🧊 ISOLATED → {service}")
            self.disabled.add(service)
            return

        log(f"🔁 RESTART → {service}")

        try:
            self.processes[service].terminate()
        except:
            pass

        time.sleep(1)

        proc = safe_launch(service)
        if proc:
            self.processes[service] = proc
            self.restarts[service] += 1

    def monitor(self):
        while True:
            time.sleep(3)

            for service, proc in list(self.processes.items()):
                if proc.poll() is not None:
                    log(f"💀 DEAD → {service}")
                    self.restart(service)
                else:
                    log(f"✅ ACTIVE → {service}")

# ---------------------------
# ENTRY
# ---------------------------

if __name__ == "__main__":
    OmegaSystemD3Kernel().boot()
