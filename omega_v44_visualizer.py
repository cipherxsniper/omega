import time
import os
import json

STATE_FILE = "omega_shared_state.json"

# ---------------------------
# LOAD STATE
# ---------------------------

def load():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# ---------------------------
# RENDER NETWORK
# ---------------------------

def render():
    os.system("clear")

    state = load()

    print("🧠 OMEGA v44 LIVE NETWORK VIEW\n")

    nodes = state.get("nodes", {})
    messages = state.get("messages", [])

    print(f"📦 Nodes: {len(nodes)}")
    print(f"📡 Messages: {len(messages)}\n")

    print("🔗 NODE MAP:\n")

    for n in list(nodes.keys())[:15]:
        print(f" - {n}")

    print("\n📡 RECENT MESSAGES:\n")

    for m in messages[-5:]:
        print(f"{m['msg']}")

# ---------------------------
# LOOP
# ---------------------------

if __name__ == "__main__":
    while True:
        render()
        time.sleep(3)
