import os
import time
import subprocess
from collections import defaultdict, deque

print("\n🧠 OMEGA SYSTEMD v2 (DEPENDENCY GRAPH KERNEL)\n")


# =========================
# DISCOVERY
# =========================
OMEGA_ROOT = os.path.expanduser("~/Omega")

def discover_modules():
    modules = []
    for root, _, files in os.walk(OMEGA_ROOT):
        for f in files:
            if f.endswith(".py") and "omega_" in f:
                modules.append(os.path.join(root, f))
    return modules


# =========================
# CLASSIFICATION (SYSTEM LAYERS)
# =========================
LAYER_MAP = {
    "kernel": 0,
    "runtime": 0,
    "identity": 1,
    "execution": 1,
    "brain": 2,
    "meta": 2,
    "learning": 2,
    "swarm": 3,
    "mesh": 3,
    "orchestrator": 3,
    "engine": 2,
    "default": 4
}


def classify(module):
    name = os.path.basename(module)

    for key in LAYER_MAP:
        if key in name:
            return LAYER_MAP[key]

    return LAYER_MAP["default"]


# =========================
# BUILD DEPENDENCY GRAPH
# =========================
def build_graph(modules):
    graph = defaultdict(list)
    layers = defaultdict(list)

    for m in modules:
        layer = classify(m)
        layers[layer].append(m)

    # dependency rule:
    # lower layer must start first
    sorted_layers = sorted(layers.keys())

    ordered = []
    for l in sorted_layers:
        ordered.extend(layers[l])

    return ordered, layers


# =========================
# SAFE LAUNCH
# =========================
def launch(module):
    name = os.path.basename(module)

    print(f"🚀 START: {name}")

    try:
        p = subprocess.Popen(
            ["python", module],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return p

    except Exception as e:
        print(f"❌ FAILED: {name} -> {e}")
        return None


# =========================
# BOOT SEQUENCE (PHASED)
# =========================
def boot():
    modules = discover_modules()
    ordered, layers = build_graph(modules)

    print(f"📦 Modules discovered: {len(modules)}")
    print(f"🧠 Boot layers: {len(layers)}\n")

    processes = {}

    # =========================
    # PHASED BOOT
    # =========================
    for layer in sorted(layers.keys()):

        print(f"\n🧩 LAYER {layer} START\n")

        for module in layers[layer]:
            p = launch(module)
            if p:
                processes[module] = p
            time.sleep(0.2)

        print(f"\n🟢 LAYER {layer} COMPLETE\n")

        # stability buffer between layers
        time.sleep(2)

    # =========================
    # SUPERVISION LOOP
    # =========================
    print("\n🧠 SYSTEMD v2 ACTIVE (GRAPH MODE)\n")

    while True:
        time.sleep(5)

        dead = []

        for m, p in processes.items():
            if p.poll() is not None:
                dead.append(m)

        if dead:
            print(f"⚠️ DEAD NODES: {len(dead)}")

        # restart only same layer (no cross-layer contamination)
        for m in dead:
            print(f"🔁 RESTART (isolated): {os.path.basename(m)}")
            p = launch(m)
            if p:
                processes[m] = p


if __name__ == "__main__":
    boot()
