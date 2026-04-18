import json
import time
import threading

STATE_FILE = "omega_shared_state.json"

STATE = {
    "nodes": {},
    "messages": [],
    "global_memory": {}
}

# ---------------------------
# WRITE STATE
# ---------------------------

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(STATE, f, indent=2)

# ---------------------------
# UPDATE MEMORY
# ---------------------------

def update_memory(key, value):
    STATE["global_memory"][key] = {
        "value": value,
        "timestamp": time.time()
    }
    save_state()

# ---------------------------
# LOG MESSAGE
# ---------------------------

def log_message(msg):
    STATE["messages"].append({
        "msg": msg,
        "time": time.time()
    })
    save_state()

# ---------------------------
# MEMORY LOOP
# ---------------------------

def memory_loop():
    while True:
        save_state()
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=memory_loop, daemon=True).start()

    update_memory("system", "omega_v43_active")

    while True:
        time.sleep(1)
