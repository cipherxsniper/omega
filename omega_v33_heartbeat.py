import time

HEARTBEAT_LOG = "omega_v33_heartbeat.log"

def pulse(node):
    entry = f"{time.time()} | {node} | ALIVE\n"

    with open(HEARTBEAT_LOG, "a") as f:
        f.write(entry)

    return entry
