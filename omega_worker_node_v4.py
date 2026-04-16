# OMEGA WORKER NODE v4
# Pure executor node for Omega Event Bus v4

import time
import uuid
from pathlib import Path

from omega_event_bus_v4 import BUS, create_event


# =========================================================
# WORKER IDENTITY
# =========================================================
WORKER_ID = f"worker_{uuid.uuid4().hex[:8]}"


# =========================================================
# TASK EXECUTION ENGINE
# =========================================================
def execute_task(event):
    """
    Safe execution layer (NO system access, only logic)
    """

    task = event.payload.get("task")
    data = event.payload.get("data", {})

    # -------------------------
    # SIMPLE TASK ROUTER
    # -------------------------
    if task == "ping":
        return {"result": "pong", "worker": WORKER_ID}

    if task == "add":
        a = data.get("a", 0)
        b = data.get("b", 0)
        return {"result": a + b, "worker": WORKER_ID}

    if task == "echo":
        return {"result": data, "worker": WORKER_ID}

    return {"error": "unknown_task", "task": task}


# =========================================================
# EVENT HANDLER
# =========================================================
def on_task(event):
    print(f"[Ω WORKER {WORKER_ID}] received task: {event.payload}")

    result = execute_task(event)

    # publish result back to bus
    BUS.publish(create_event(
        "task_result",
        WORKER_ID,
        {
            "task_id": event.id,
            "output": result
        }
    ))


# =========================================================
# HEARTBEAT LOOP
# =========================================================
def heartbeat():
    while True:
        BUS.publish(create_event(
            "heartbeat",
            WORKER_ID,
            {"status": "alive"}
        ))
        time.sleep(5)


# =========================================================
# BOOT WORKER
# =========================================================
def start_worker():
    print(f"[Ω WORKER {WORKER_ID}] online | role=executor")

    # subscribe to tasks
    BUS.subscribe("task", on_task)

    # heartbeat thread (non-blocking loop style)
    import threading
    threading.Thread(target=heartbeat, daemon=True).start()

    # keep alive
    while True:
        time.sleep(1)


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    start_worker()
