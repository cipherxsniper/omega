import time
from omega.core.global_memory import GLOBAL_MEMORY

def monitor_health():
    while True:
        packets = GLOBAL_MEMORY["packets"]

        if len(packets) > 0:
            last = packets[-1]

            # detect stagnation
            if last.get("type") is None:
                last["type"] = "auto_repaired_signal"

        time.sleep(1)
