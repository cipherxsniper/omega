import os
import re
import time
import subprocess
from pathlib import Path

ROOT = Path.home() / "Omega"

MAX_MODULES = 25
BATCH_SIZE = 10
BATCH_DELAY = 4

# ---------------------------
# 1. PRIORITY CORE SYSTEM
# ---------------------------
PRIORITY_KEYWORDS = [
    "unified",
    "brain",
    "kernel",
    "governor",
    "assistant",
    "orchestrator",
    "memory",
    "identity",
    "mesh",
    "execution",
    "learning",
    "self",
    "cognitive",
]

EXCLUDE = [
    "test",
    "backup",
    "patch",
    "old",
    "deprecated",
    "log",
    "tmp"
]


def version_score(name: str):
    """Extract highest version number in filename"""
    nums = re.findall(r"v(\d+)", name)
    return max(map(int, nums)) if nums else 0


def is_valid(name: str):
    lower = name.lower()
    if not lower.endswith(".py"):
        return False
    if any(x in lower for x in EXCLUDE):
        return False
    return True


def priority_score(name: str):
    score = version_score(name)

    for i, key in enumerate(PRIORITY_KEYWORDS):
        if key in name.lower():
            score += (len(PRIORITY_KEYWORDS) - i) * 10

    return score


def discover_modules():
    modules = []

    for root, _, files in os.walk(ROOT):
        for f in files:
            if is_valid(f):
                modules.append(Path(root) / f)

    return modules


def select_best(modules):
    ranked = sorted(modules, key=lambda m: priority_score(m.name), reverse=True)

    selected = []
    seen = set()

    for m in ranked:
        base = re.sub(r"_v\d+.*", "", m.name)

        if base in seen:
            continue

        seen.add(base)
        selected.append(m)

        if len(selected) >= MAX_MODULES:
            break

    return selected


def launch(module_path: Path):
    try:
        return subprocess.Popen(["python", str(module_path)])
    except Exception as e:
        print(f"❌ Failed: {module_path} -> {e}")
        return None


def boot():
    print("\n🧠 OMEGA GOVERNANCE BOOT v1 (CONTROLLED MODE)\n")

    modules = discover_modules()
    selected = select_best(modules)

    print(f"📦 Total discovered: {len(modules)}")
    print(f"🎯 Selected core modules: {len(selected)} (MAX {MAX_MODULES})\n")

    batch = []
    batch_count = 0

    for m in selected:
        batch.append(m)

        if len(batch) >= BATCH_SIZE:
            batch_count += 1
            print(f"\n🧩 BATCH {batch_count} START\n")

            for mod in batch:
                print(f"🚀 START: {mod.name}")
                launch(mod)
                time.sleep(0.3)

            print(f"\n🟢 BATCH {batch_count} COMPLETE")
            time.sleep(BATCH_DELAY)
            batch = []

    if batch:
        batch_count += 1
        print(f"\n🧩 FINAL BATCH {batch_count}\n")

        for mod in batch:
            print(f"🚀 START: {mod.name}")
            launch(mod)
            time.sleep(0.3)

    print("\n🧠 OMEGA GOVERNANCE BOOT COMPLETE")
    print("🔒 Running in controlled 25-module ecosystem")


if __name__ == "__main__":
    boot()
