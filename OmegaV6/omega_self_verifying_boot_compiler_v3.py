import os
import sys
import time
import subprocess
from pathlib import Path
import importlib.util

ROOT = Path.home() / "Omega"
OMEGA_V6 = ROOT / "OmegaV6"

# =========================================================
# 1. DISCOVERY LAYER
# =========================================================

def discover_modules(base_dir):
    modules = []

    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".py") and not f.startswith("__"):
                full_path = Path(root) / f
                modules.append(full_path)

    return modules


# =========================================================
# 2. IMPORT + SYNTAX VERIFICATION
# =========================================================

def verify_syntax(file_path):
    try:
        source = Path(file_path).read_text()
        compile(source, str(file_path), "exec")
        return True, None
    except Exception as e:
        return False, str(e)


# =========================================================
# 3. EXECUTION TYPE CLASSIFIER (minimal safe version)
# =========================================================

def classify_module(name):
    if "orchestrator" in name or "bus" in name:
        return "SERVICE"
    if "memory" in name or "graph" in name:
        return "CORE_TASK"
    if "repair" in name or "patch" in name:
        return "TASK"
    return "TASK"


# =========================================================
# 4. DEPENDENCY ORDERING (simple causal priority)
# =========================================================

BOOT_PRIORITY = [
    "core",
    "memory",
    "bus",
    "graph",
    "runtime",
    "orchestrator"
]


def priority_score(path):
    name = str(path).lower()
    score = 100

    for i, key in enumerate(BOOT_PRIORITY):
        if key in name:
            score -= i * 10

    return score


# =========================================================
# 5. SAFE LAUNCHER
# =========================================================

def safe_launch(file_path):
    try:
        print(f"\n🚀 Launching: {file_path}")

        result = subprocess.Popen(
            [sys.executable, str(file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        time.sleep(1)

        if result.poll() is None:
            print("🟢 RUNNING (service detected)")
            return True
        else:
            out, err = result.communicate()
            print("🔴 EXITED")
            print(err.decode()[:300])
            return False

    except Exception as e:
        print("❌ LAUNCH FAILED:", e)
        return False


# =========================================================
# 6. BOOT COMPILER CORE
# =========================================================

def boot_system():
    print("\n🧠 OMEGA SELF-VERIFYING BOOT COMPILER v3\n")

    modules = discover_modules(OMEGA_V6)

    # sort by causal priority
    modules.sort(key=priority_score)

    verified = []
    failed = []

    # STEP 1: VERIFY
    for m in modules:
        ok, err = verify_syntax(m)

        if ok:
            verified.append(m)
        else:
            failed.append((m, err))

    print(f"\n📦 VERIFIED MODULES: {len(verified)}")
    print(f"❌ FAILED MODULES: {len(failed)}")

    # STEP 2: REPORT FAILURES
    for f, err in failed:
        print("\n──────── ERROR MODULE ────────")
        print(f)
        print(err[:200])

    # STEP 3: BOOT SEQUENCE
    print("\n🚀 BOOT SEQUENCE STARTING...\n")

    running = []

    for m in verified:
        name = m.name.lower()

        # skip logs/config dumps
        if "log" in name or "__pycache__" in str(m):
            continue

        ok = safe_launch(m)

        if ok:
            running.append(m)

    # STEP 4: SYSTEM SUMMARY
    print("\n══════════════════════════════")
    print("🧠 BOOT COMPLETE SUMMARY")
    print(f"TOTAL MODULES : {len(modules)}")
    print(f"VERIFIED      : {len(verified)}")
    print(f"RUNNING       : {len(running)}")
    print(f"FAILED        : {len(failed)}")

    if len(running) < len(verified) * 0.5:
        print("\n⚠️ SYSTEM DEGRADED STATE")
    else:
        print("\n🟢 SYSTEM STABLE")


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    boot_system()
