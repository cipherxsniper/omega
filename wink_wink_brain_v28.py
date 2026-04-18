from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
from omega_global_thought_bus_v23 import register_node, broadcast, get_recent, get_global_state
# WINK_WINK BRAIN v28 — STABLE FIXED LOOP

import time
from omega_global_thought_bus_v24 import run_observer

VERSION = "v28"

NODE_NAME = "wink_wink_v28"
register_node(NODE_NAME)

NODE_ID = "wink_wink_brain_v28.py" 
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

def global_novelty(sentence):
    recent = get_recent(20)
    overlap = 0

    for s in recent:
        if len(set(sentence.split()) & set(s.split())) > 5:
            overlap += 1

    return 1.0 - min(overlap * 0.2, 1.0)

