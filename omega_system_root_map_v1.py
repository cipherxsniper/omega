import os
from pathlib import Path
import json

# ================================
# OMEGA SYSTEM ROOT MAPPER v1
# SELF-DISCOVERING MODULE INDEX
# ================================

OMEGA_ROOTS = [
    Path.home() / "Omega",
    Path.home() / "Omega" / "OmegaV6",
]

IGNORE_DIRS = {
    "__pycache__",
    ".git",
    "node_modules",
    "tmp",
    "logs",
}

def is_valid_module(file):
    return file.endswith(".py")

def scan_root(root: Path):
    modules = {}

    for path in root.rglob("*"):
        if any(ignore in path.parts for ignore in IGNORE_DIRS):
            continue

        if path.is_file() and is_valid_module(path.name):
            name = path.stem

            modules[name] = {
                "path": str(path),
                "root": str(root),
            }

    return modules


def build_system_map():
    system_map = {}

    print("\n🧠 OMEGA SYSTEM ROOT MAP v1\n")

    for root in OMEGA_ROOTS:
        if not root.exists():
            continue

        print(f"🔍 Scanning: {root}")

        found = scan_root(root)
        system_map.update(found)

        print(f"✔ Found {len(found)} modules")

    return system_map


def save_map(system_map):
    out = Path.home() / "Omega" / "omega_system_root_map.json"

    with open(out, "w") as f:
        json.dump(system_map, f, indent=2)

    print("\n🧠 SYSTEM MAP SAVED")
    print(f"📦 {out}")


if __name__ == "__main__":
    system_map = build_system_map()
    save_map(system_map)
