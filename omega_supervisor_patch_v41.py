from omega_cat_patch_v41 import repair_action
import re

def approve_repair(module_name):
    # You can later make this smarter (risk scoring, etc)
    return True


def supervisor(event_type, line):
    if event_type == "missing_module":

        match = re.findall(r"No module named '([^']+)'", line)
        module_name = match[0] if match else "unknown"

        if approve_repair(module_name):
            print(f"[Ω SUPERVISOR] APPROVED repair: {module_name}")
            repair_action(event_type, {"module": module_name})
        else:
            print(f"[Ω SUPERVISOR] REJECTED repair: {module_name}")
