import os
from pathlib import Path
import glob

OMEGA_ROOT = Path.home() / "Omega"
CORE_DIR = OMEGA_ROOT / "runtime_v7" / "core"


# =====================================================
# CORE RESOLVER ENGINE
# =====================================================
def resolve_latest(patterns, grep=None):
    """
    Finds latest file matching patterns with optional version filtering.
    """

    candidates = []

    for pattern in patterns:
        candidates.extend(glob.glob(str(CORE_DIR / pattern)))

    if not candidates:
        return None

    # Optional semantic filter (v13+ etc)
    if grep:
        filtered = []
        for c in candidates:
            if any(tag in c for tag in grep):
                filtered.append(c)
        if filtered:
            candidates = filtered

    # Sort by version-aware sorting (last number wins)
    candidates.sort(key=lambda x: extract_version(x))

    return candidates[-1]


def extract_version(path):
    """
    Extract numeric version from filename safely.
    """
    import re
    nums = re.findall(r"v(\d+)", path)
    if not nums:
        return 0
    return int(nums[-1])


# =====================================================
# SELF HEALING STACK RESOLVER
# =====================================================
def resolve_stack():
    swarm_bus = resolve_latest(
        [
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ],
        grep=["v14", "v15", "v16", "v17", "v13", "v2", "v3", "v4", "v5", "v6", "v7"]
    )

    # fallback without version bias
    if not swarm_bus:
        swarm_bus = resolve_latest([
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ])

    memory = resolve_latest([
        "omega_crdt_memory*.py",
        "omega_memory*.py",
        "omega_global_memory*.py"
    ])

    assistant = resolve_latest([
        "omega_assistant*.py",
        "omega_*assistant*.py",
        "*assistant*.py"
    ])

    emitter = str(CORE_DIR / "test_swarm_emitter.py")

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }


# =====================================================
# SELF HEALING LOGIC
# =====================================================
def self_heal(stack):
    healed = {}

    for k, v in stack.items():
        if v and os.path.exists(v):
            healed[k] = v
        else:
            healed[k] = None

    # Attempt deep fallback search if critical missing
    if not healed["swarm_bus"]:
        print("[HEAL] Deep swarm scan triggered...")
        all_buses = glob.glob(str(CORE_DIR / "**/*bus*.py"), recursive=True)

        if all_buses:
            healed["swarm_bus"] = sorted(all_buses)[-1]

    return healed


# =====================================================
# BOOT EXECUTION
# =====================================================
if __name__ == "__main__":
    print("\n🧠 [OMEGA SELF-HEALING BOOT V6]\n")

    stack = resolve_stack()
    healed_stack = self_heal(stack)

    print("\n📦 RESOLVED STACK:")
    for k, v in healed_stack.items():
        print(f"  {k}: {v}")

    missing = [k for k, v in healed_stack.items() if not v]

    if missing:
        print("\n❌ BOOT FAILED - STILL MISSING:")
        for m in missing:
            print("  -", m)
    else:
        print("\n🟢 BOOT SUCCESS - ALL SYSTEMS RESOLVED")
