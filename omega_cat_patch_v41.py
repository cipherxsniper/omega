import os
import re
from datetime import datetime

REPAIR_HISTORY = set()

VERSION_FALLBACKS = ["v9_4", "v9_3", "v9_2", "v9"]

def approve_repair(module_name):
    # SIMPLE SUPERVISOR GATE (you can later upgrade this)
    return True


def repair_action(event_type, data):
    global REPAIR_HISTORY

    if event_type != "missing_module":
        return False

    module = data.get("module", "unknown")

    if module in REPAIR_HISTORY:
        print(f"[Ω SUPERVISOR] BLOCKED duplicate repair: {module}")
        return False

    REPAIR_HISTORY.add(module)

    core_path = os.path.join(os.path.dirname(__file__), "core")
    os.makedirs(core_path, exist_ok=True)

    target = os.path.join(core_path, f"{module}.py")

    if os.path.exists(target):
        print(f"[Ω SUPERVISOR] Module already exists: {module}")
        return False

    # fallback resolution
    fallback_used = None
    base_match = re.match(r"(.*_v)(\d+)(_.*)?", module)

    if base_match:
        prefix = base_match.group(1)
        suffix = base_match.group(3) or ""

        for v in VERSION_FALLBACKS:
            candidate = f"{prefix}{v.replace('v','')}{suffix}"
            candidate_path = os.path.join(core_path, f"{candidate}.py")

            if os.path.exists(candidate_path):
                fallback_used = candidate
                break

    with open(target, "w") as f:
        f.write("# Ω AUTO-REPAIR MODULE\n\n")

        if fallback_used:
            f.write(f"# fallback routed: {fallback_used}\n")
            f.write("def subscribe(*a,**k): print('fallback active')\n")
            f.write("def publish(*a,**k): print('fallback active')\n")
        else:
            f.write("def subscribe(*a,**k): pass\n")
            f.write("def publish(*a,**k): pass\n")

    print(f"[Ω REPAIR] Created: {module} | fallback={fallback_used}")

    return True
