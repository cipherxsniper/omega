import os
import time
import subprocess
from collections import defaultdict, deque

print("\n🧠 OMEGA SYSTEMD v3 (FULL DAG ENGINE)\n")

OMEGA_ROOT = os.path.expanduser("~/Omega")


# =========================
# DISCOVERY
# =========================
def discover_modules():
    mods = []
    for root, _, files in os.walk(OMEGA_ROOT):
        for f in files:
            if f.endswith(".py") and "omega_" in f:
                mods.append(os.path.join(root, f))
    return mods


# =========================
# DEPENDENCY MODEL
# =========================
# You can extend this later dynamically from JSON/YAML
DEPENDENCIES = {
    "omega_unified_kernel_v15": [],
    "omega_identity_kernel_v25": ["omega_unified_kernel_v15"],
    "omega_execution_engine_v7": ["omega_identity_kernel_v25"],
    "omega_meta_brain_v10": ["omega_execution_engine_v7"],
    "omega_unified_brain_v22": ["omega_meta_brain_v10"],
    "omega_swarm_memory_bridge_v9": ["omega_unified_brain_v22"],
    "omega_mesh_superintelligence_v12": ["omega_swarm_memory_bridge_v9"],
}


# =========================
# BUILD DAG
# =========================
def build_dag(modules):
    graph = defaultdict(list)
    indegree = defaultdict(int)

    name_map = {}

    def name_of(path):
        return os.path.basename(path).replace(".py", "")

    for m in modules:
        name_map[name_of(m)] = m

    for m in modules:
        node = name_of(m)

        deps = DEPENDENCIES.get(node, [])
        indegree[node] = indegree.get(node, 0)

        for d in deps:
            graph[d].append(node)
            indegree[node] += 1

    return graph, indegree, name_map


# =========================
# TOPOLOGICAL SORT (KAHN)
# =========================
def resolve_order(graph, indegree):
    q = deque([n for n in indegree if indegree[n] == 0])
    order = []

    while q:
        node = q.popleft()
        order.append(node)

        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)

    if len(order) != len(indegree):
        print("⚠️ DAG CYCLE DETECTED — aborting unsafe execution")
        return []

    return order


# =========================
# LAUNCH
# =========================
def launch(path):
    name = os.path.basename(path)
    print(f"🚀 START: {name}")

    try:
        return subprocess.Popen(
            ["python", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"❌ FAIL {name}: {e}")
        return None


# =========================
# BOOT ENGINE
# =========================
def boot():
    modules = discover_modules()

    print(f"📦 Modules discovered: {len(modules)}")

    graph, indegree, name_map = build_dag(modules)
    order = resolve_order(graph, indegree)

    if not order:
        return

    processes = {}

    print("\n🧩 DAG BOOT SEQUENCE START\n")

    # =========================
    # STAGED EXECUTION
    # =========================
    for node in order:
        path = name_map.get(node)
        if not path:
            continue

        p = launch(path)
        if p:
            processes[node] = p

        time.sleep(0.2)

    print("\n🟢 DAG BOOT COMPLETE\n")
    print("🧠 SYSTEMD v3 ACTIVE (DEPENDENCY GRAPH MODE)\n")

    # =========================
    # WATCHDOG LOOP
    # =========================
    while True:
        time.sleep(5)

        for node, proc in list(processes.items()):
            if proc.poll() is not None:
                print(f"⚠️ NODE DEAD: {node} → restarting")

                path = name_map.get(node)
                if path:
                    processes[node] = launch(path)


if __name__ == "__main__":
    boot()
