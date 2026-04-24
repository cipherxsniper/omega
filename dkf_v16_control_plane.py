import requests
import time
import os
import subprocess
import json

OLLAMA = "http://127.0.0.1:11434"
STATE_FILE = os.path.expanduser("~/Omega/dkf_control_state.json")


# -----------------------------
# STATE
# -----------------------------
def load_state():
    if not os.path.exists(STATE_FILE):
        return {"running": True, "last_ok": time.time()}
    try:
        return json.load(open(STATE_FILE))
    except:
        return {"running": True, "last_ok": time.time()}


def save_state(state):
    json.dump(state, open(STATE_FILE, "w"))


# -----------------------------
# HEALTH CHECK
# -----------------------------
def ollama_alive():
    try:
        r = requests.get(f"{OLLAMA}/api/tags", timeout=3)
        return r.status_code == 200
    except:
        return False


# -----------------------------
# MODEL SAFE CALL
# -----------------------------
def test_model():
    try:
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={
                "model": "tinyllama:latest",
                "prompt": "ping",
                "stream": False
            },
            timeout=10
        )
        return "response" in r.json()
    except:
        return False


# -----------------------------
# CONTROL LOOP
# -----------------------------
def restart_ollama():
    print("🤖 Restart signal issued for Ollama (manual Termux restart required)")


def control_loop():
    print("🧠 DKF v16 CONTROL PLANE ONLINE")

    state = load_state()

    while True:
        alive = ollama_alive()
        model_ok = test_model() if alive else False

        if not alive:
            print("⚠️ Ollama not reachable")
        elif not model_ok:
            print("⚠️ Model failing - check memory / load state")
        else:
            print("✅ System healthy")

        state["last_ok"] = time.time() if alive else state["last_ok"]
        save_state(state)

        # auto recovery logic
        if not alive:
            print("🔁 Recovery mode engaged... retrying in 5s")

        time.sleep(5)


if __name__ == "__main__":
    control_loop()
