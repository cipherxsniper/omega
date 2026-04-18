import os
import re
import time
import json
from collections import defaultdict

OMEGA_ROOTS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

STATE_FILE = "omega_v39_graph.json"

# ---------------------------
# IMPORT PARSER
# ---------------------------

IMPORT_RE = re.compile(r'^\s*(import\s+\w+|from\s+[\w\.]+\s+import\s+)', re.MULTILINE)

def extract_imports(file_path):
    try:
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()
        return IMPORT_RE.findall(content)
    except:
        return []

# ---------------------------
# GRAPH BUILDER
# ---------------------------

def build_graph():
    graph = defaultdict(list)
    files = []

    for root_dir in OMEGA_ROOTS:
        if not os.path.exists(root_dir):
            continue

        for root, _, fs in os.walk(root_dir):
            for f in fs:
                if f.endswith(".py"):
                    full = os.path.join(root, f)
                    files.append(full)

    for file in files:
        imports = extract_imports(file)
        for imp in imports:
            graph[file].append(imp.strip())

    return graph

# ---------------------------
# ANALYSIS
# ---------------------------

def analyze(graph):
    total_nodes = len(graph)
    edges = sum(len(v) for v in graph.values())

    orphans = [k for k, v in graph.items() if len(v) == 0]

    return {
        "nodes": total_nodes,
        "edges": edges,
        "orphans": orphans[:10],
    }

# ---------------------------
# VISUALIZER
# ---------------------------

def render(graph):
    print("\n🧠 OMEGA DEPENDENCY GRAPH (v39)")
    print("=" * 60)

    for node, deps in list(graph.items())[:20]:
        name = os.path.basename(node)
        print(f"\n📦 {name}")
        for d in deps[:5]:
            print(f"   └── {d}")

# ---------------------------
# STATE
# ---------------------------

def save_state(graph):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({k: v for k, v in graph.items()}, f, indent=2)
    except:
        pass

# ---------------------------
# MAIN LOOP
# ---------------------------

def run():
    print("🧠 Omega v39 Dependency Engine ONLINE")

    while True:
        graph = build_graph()
        report = analyze(graph)

        render(graph)

        print("\n📊 SYSTEM SUMMARY")
        print(f"Nodes: {report['nodes']}")
        print(f"Edges: {report['edges']}")
        print(f"Orphan modules: {len(report['orphans'])}")

        if report["orphans"]:
            print("\n⚠️ Orphan nodes detected:")
            for o in report["orphans"]:
                print("  -", os.path.basename(o))

        save_state(graph)

        print("\n⏳ Next scan in 5s...\n")
        time.sleep(5)

if __name__ == "__main__":
    run()
