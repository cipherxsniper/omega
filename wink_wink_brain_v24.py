from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
# WINK_WINK BRAIN v24 — UNIFIED CORE TEMPLATE

import time
from omega_global_thought_bus_v24 import run_observer

VERSION = "v24"

NODE_ID = "wink_wink_brain_v24.py" 
register(NODE_ID)

while True:
    def anti_loop(msg, hist):
        return msg not in hist[-10:]

    history = []
    recent = fetch_recent(5)
    if recent:
        influence = sum(m["signal"] for m in recent) / len(recent)
        try:
            signal = (signal + influence) / 2
        except:
            pass
    try:
        output = run_observer(f"wink_wink_brain_{VERSION}")
        publish(NODE_ID, output, state, signal)
        time.sleep(1)
    except KeyboardInterrupt:
        break
