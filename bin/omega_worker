#!/usr/bin/env python3
# ==========================================
# OMEGA CORE STACK v4
# WORKER NODE (PURE EXECUTOR)
# ==========================================

import os
import time
import uuid
import json
import queue
import threading
from pathlib import Path

# -----------------------------
# CORE IDENTITY
# -----------------------------
WORKER_ID = str(uuid.uuid4())[:8]
WORKER_ROLE = os.getenv("OMEGA_ROLE", "executor")

BASE_DIR = Path(__file__).resolve().parents[2]
EVENT_FILE = BASE_DIR / "runtime" / "event_bus.jsonl"
HEARTBEAT_FILE = BASE_DIR / "runtime" / f"worker_{WORKER_ID}_heartbeat.json"


# -----------------------------
# SAFE FILE INIT
# -----------------------------
def ensure_runtime():
    (BASE_DIR / "runtime").mkdir(parents=True, exist_ok=True)


# -----------------------------
# HEARTBEAT SYSTEM
# -----------------------------
def heartbeat():
    while True:
        try:
            data = {
                "worker_id": WORKER_ID,
                "role": WORKER_ROLE,
                "status": "alive",
                "timestamp": time.time()
            }

            HEARTBEAT_FILE.write_text(json.dumps(data))
        except Exception:
            pass

        time.sleep(2)


# -----------------------------
# EVENT CONSUMER
# -----------------------------
def read_events():
    if not EVENT_FILE.exists():
        return []

    try:
        lines = EVENT_FILE.read_text().splitlines()
        return [json.loads(l) for l in lines[-50:]]
    except Exception:
        return []


# -----------------------------
# EXECUTION ENGINE
# -----------------------------
def execute_task(task):
    """
    Pure deterministic executor.
    NO imports, NO recursion.
    """

    action = task.get("action")
    payload = task.get("payload", {})

    if action == "ping":
        return {"status": "pong", "worker": WORKER_ID}

    if action == "echo":
        return {"echo": payload, "worker": WORKER_ID}

    if action == "compute":
        # safe sandbox computation
        try:
            expr = payload.get("expr", "")
            result = eval(expr, {"__builtins__": {}})
            return {"result": result, "worker": WORKER_ID}
        except Exception as e:
            return {"error": str(e), "worker": WORKER_ID}

    return {"status": "unknown_task", "worker": WORKER_ID}


# -----------------------------
# MAIN LOOP
# -----------------------------
def run():
    ensure_runtime()

    print(f"[Ω WORKER {WORKER_ID}] online | role={WORKER_ROLE}")

    threading.Thread(target=heartbeat, daemon=True).start()

    last_index = 0

    while True:
        events = read_events()

        if len(events) > last_index:
            new_events = events[last_index:]
            last_index = len(events)

            for event in new_events:
                if event.get("target") in [WORKER_ROLE, "all"]:
                    result = execute_task(event)

                    print(f"[Ω WORKER {WORKER_ID}] executed:", result)

        time.sleep(1)


if __name__ == "__main__":
    run()
