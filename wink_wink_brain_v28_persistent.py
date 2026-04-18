from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import time
import random
from wink_wink_language_core_v25 import generate_sentence

def analyze():
    # replace later with real signal system
    return {
        "signal": random.uniform(0.2, 0.95),
        "reward": random.uniform(0.4, 1.0),
        "state": "ACTIVE_LEARNING"
    }

NODE_ID = "wink_wink_brain_v28_persistent.py" 
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
    metrics = analyze()
    publish(NODE_ID, generate_sentence(metrics))
    time.sleep(1)
