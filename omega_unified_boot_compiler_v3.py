import json
import os
import subprocess
import time
from pathlib import Path

# ================================
# UNIFIED OMEGA BOOT COMPILER v3
# SELF-DISCOVERING EXECUTION ENGINE
# ================================

OMEGA_ROOT = Path.home() / "Omega"
MAP_FILE = OMEGA_ROOT / "omega_system_root_map.json"
LOG_DIR = OMEGA_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ================================
# LOAD SYSTEM MAP
# ================================
def load_map():
    if not MAP_FILE.exists():
        print("❌ System map not found. Run omega_system_root_map_v1.py first.")
        exit()

    with open(MAP_FILE, "r") as f:
        return json.load(f)

# ================================
# BOOT PRIORITY KEYWORDS
# ================================
BOOT_PRIORITY = [
    "execution",
    "identity",
    "runtime",
    "introspection",
    "self_aware",
    "kernel",
    "memory",
    "mesh",
    "brain",
    "assistant",
    "cognitive",
]

# ================================
# SCORE MODULE IMPORTANCE
# ================================
def score_module(name):
    score = 0
    for i, key in enumerate(BOOT_PRIORITY):
        if key in name:
            score += (len(BOOT_PRIORITY) - i)
    return score

# ================================
# BUILD EXECUTION GRAPH
# ================================
def build_execution_graph(system_map):
    modules = list(system_map.items())

    ranked = sorted(
        modules,
        key=lambda x: score_module(x[0]),
        reverse=True
    )

    return ranked

# ================================
# LAUNCH MODULE
# ================================
def launch(name, meta):
    path = meta["path"]

    log_file = LOG_DIR / f"{name}.log"

    cmd = f"nohup python {path} > {log_file} 2>&1 &"
    os.system(cmd)

    print(f"🚀 BOOT: {name}")

# ================================
# BOOT SEQUENCE ENGINE
# ================================
        time.sleep(10)
        print("🟢 Omega v3 heartbeat: system stable")


if __name__ == "__main__":
    boot()
