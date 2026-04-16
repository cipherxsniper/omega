from omega_repair_reasoning_v42 import repair_reasoning
import re


def approve_repair(module):
    # smarter gate (can be expanded later)
    return True


def supervisor(event_type, line):

    if event_type != "missing_module":
        return

    match = re.findall(r"No module named '([^']+)'", line)
    module = match[0] if match else "unknown"

    if approve_repair(module):
        print(f"[Ω SUPERVISOR v4.2] APPROVED: {module}")
        repair_reasoning(event_type, {"module": module})
    else:
        print(f"[Ω SUPERVISOR v4.2] REJECTED: {module}")
