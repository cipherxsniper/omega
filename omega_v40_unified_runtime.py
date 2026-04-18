import os
import re
import time
import json
from collections import defaultdict

OMEGA_ROOTS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

STATE_FILE = "omega_v40_state.json"

IMPORT_RE = re.compile(r'^\s*(import\s+\w+|from\s+[\w\.]+\s+import\s+)', re.MULTILINE)

# ---------------------------
# FILE SCAN
# ---------------------------

def get_python_files():
    files = []
    for root_dir in OMEGA_ROOTS:
        if not os.path.exists(root_dir):
            continue

        for root, _, fs in os.walk(root_dir):
            for f in fs:
                if f.endswith(".py"):
                    files.append(os.path.join(root, f))
    return files

# ---------------------------
# IMPORT EXTRACTION
# ---------------------------

def extract_imports(file_path):
    try:
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()
        return IMPORT_RE.findall(content)
    except:
        return []

# ---------------------------
# GRAPH ENGINE
# ---------------------------

def build_dependency_graph(files):
    graph = defaultdict(list)

    for f in files:
        imports = extract_imports(f)
        for imp in imports:
            graph[f].append(imp.strip())

    return graph

# ---------------------------
# PLUGIN CLASSIFIER
# ---------------------------

def classify_plugin(file):
    name = os.path.basename(file)

    if "core" in name:
        return "CORE_PLUGIN"
    if "agent" in name or "brain" in name:
        return "AGENT_PLUGIN"
    if "util" in name or "tool" in name:
        return "UTILITY_PLUGIN"
    return "GENERAL_PLUGIN"

# ---------------------------
# AUTO HEAL ANALYZER (SAFE ONLY)
# ---------------------------

def analyze_health(graph):
    issues = []

    for node, deps in graph.items():
        if len(deps) == 0:
            issues.append({
                "file": node,
                "issue": "NO_IMPORTS_FOUND (isolated node)"
            })

    return issues

# ---------------------------
# VISUALIZER
# ---------------------------

def render(graph, plugins):
    print("\n🧠 OMEGA v40 UNIFIED RUNTIME")
    print("=" * 70)

    for node, deps in list(graph.items())[:15]:
        print(f"\n📦 {os.path.basename(node)} [{plugins[node]}]")
        for d in deps[:5]:
            print(f"   └── {d}")

# ---------------------------
# STATE
# ---------------------------

def save_state(data):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

# ---------------------------
# MAIN LOOP
# ---------------------------

def run():
    print("🧠 Omega v40 Unified Runtime ONLINE")

    while True:
        files = get_python_files()

        graph = build_dependency_graph(files)

        plugins = {f: classify_plugin(f) for f in files}

        health = analyze_health(graph)

        render(graph, plugins)

        print("\n📊 SYSTEM SUMMARY")
        print(f"Total Python Nodes: {len(files)}")
        print(f"Graph Edges: {sum(len(v) for v in graph.values())}")

        print(f"Issues Detected: {len(health)}")

        if health:
            print("\n🛟 AUTO-HEAL REPORT:")
            for h in health[:10]:
                print(f" - {os.path.basename(h['file'])}: {h['issue']}")

        print("\n🧠 SYSTEM STATE:")
        print("Single unified runtime active (no multi-brain conflict)")

        save_state({
            "files": len(files),
            "edges": sum(len(v) for v in graph.values()),
            "issues": health
        })

        time.sleep(5)

if __name__ == "__main__":
    run()
