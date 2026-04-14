import time
from collections import defaultdict, deque

# =========================
# OMEGA DEPENDENCY SCHEDULER v1
# =========================

# HARD RULE:
# kernel → identity → memory → brain → swarm → mesh → economy → governance

DEPENDENCY_GRAPH = {
    "omega_unified_kernel_v15.py": [],
    "omega_identity_kernel_v25.py": ["omega_unified_kernel_v15.py"],

    "omega_execution_engine_v7.py": ["omega_identity_kernel_v25.py"],
    "omega_meta_brain_v10.py": ["omega_execution_engine_v7.py"],

    "omega_unified_brain_v22.py": ["omega_meta_brain_v10.py"],
    "omega_swarm_memory_bridge_v9.py": ["omega_unified_brain_v22.py"],

    "omega_mesh_superintelligence_v12.py": ["omega_swarm_memory_bridge_v9.py"],
    "omega_process_supervisor_v1.py": ["omega_mesh_superintelligence_v12.py"],
}


def topo_sort(graph):
    indeg = defaultdict(int)
    adj = defaultdict(list)

    for node, deps in graph.items():
        for d in deps:
            adj[d].append(node)
            indeg[node] += 1

    q = deque([n for n in graph if indeg[n] == 0])
    order = []

    while q:
        n = q.popleft()
        order.append(n)

        for nxt in adj[n]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)

    return order


def launch(module):
    print(f"🚀 READY TO LAUNCH: {module}")
    # intentionally separated (scheduler does NOT execute directly)


def boot():
    print("\n🧠 OMEGA DEPENDENCY GRAPH SCHEDULER v1\n")

    order = topo_sort(DEPENDENCY_GRAPH)

    print("📊 Execution Order:\n")

    for i, m in enumerate(order):
        print(f"{i+1}. {m}")

        launch(m)
        time.sleep(1.5)  # controlled pacing

    print("\n🧠 DEPENDENCY GRAPH COMPLETE (ORDER ENFORCED)\n")


if __name__ == "__main__":
    boot()
