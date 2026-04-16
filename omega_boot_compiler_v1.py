import os
import subprocess
from pathlib import Path
from collections import defaultdict

ROOT = Path.home() / "Omega"

# ==============================
# DISCOVERY ENGINE
# ==============================

def scan_modules():
    modules = []

    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.startswith("omega_") and f.endswith(".py"):
                modules.append(Path(root) / f)

    return modules


# ==============================
# CLASSIFIER
# ==============================

def classify(module_name):
    name = module_name.lower()

    if any(x in name for x in ["kernel", "bus", "orchestrator", "brain", "engine"]):
        return "SERVICE"

    if any(x in name for x in ["repair", "patch", "analyze", "import", "fix"]):
        return "TASK"

    return "HYBRID"


# ==============================
# LAYER MAPPER (CAUSAL ORDER)
# ==============================

def assign_layer(module_name):
    name = module_name.lower()

    if "identity" in name or "execution" in name:
        return 0
    if "memory" in name:
        return 1
    if "runtime" in name or "introspect" in name:
        return 2
    if "graph" in name or "causal" in name:
        return 3
    if "predict" in name:
        return 4
    if "consensus" in name or "truth" in name:
        return 5
    if "repair" in name or "heal" in name:
        return 6
    if "boot" in name or "orchestrator" in name:
        return 7

    return 99


# ==============================
# COMPILER
# ==============================

def compile_boot_plan(modules):
    plan = defaultdict(list)

    for m in modules:
        layer = assign_layer(m.name)
        plan[layer].append(m)

    return dict(sorted(plan.items()))


# ==============================
# EXECUTOR
# ==============================

def run_module(path):
    try:
        print(f"\n🚀 RUN: {path.name}")
        subprocess.run(["python", str(path)], check=False)
    except Exception as e:
        print(f"❌ ERROR: {path.name} → {e}")


# ==============================
# BOOT COMPILER
# ==============================

def boot():
    print("\n🧠 OMEGA BOOT COMPILER v1\n")

    modules = scan_modules()
    plan = compile_boot_plan(modules)

    print(f"📦 MODULES FOUND: {len(modules)}")

    for layer, mods in plan.items():

        print("\n────────────────────────")
        print(f"🧬 LAYER {layer}")
        print("────────────────────────")

        for m in mods:
            role = classify(m.name)
            print(f" - {m.name} [{role}]")

        for m in mods:
            run_module(m)


# ==============================
# ENTRY
# ==============================

if __name__ == "__main__":
    boot()
