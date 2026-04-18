import os
import socket
import json
import time
import threading

BUS_HOST = "127.0.0.1"
BUS_PORT = 5051

ROOT = os.path.expanduser("~/Omega")

# ---------------------------
# REGISTER NODE
# ---------------------------

def register_node(file_path):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((BUS_HOST, BUS_PORT))

        msg = {
            "from": file_path,
            "type": "register",
            "data": {
                "status": "online",
                "timestamp": time.time()
            }
        }

        s.send(json.dumps(msg).encode())
        s.close()

    except Exception as e:
        pass

# ---------------------------
# SCAN & REGISTER ALL NODES
# ---------------------------

def scan_and_register():
    for r, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".py"):
                register_node(os.path.join(r, f))

# ---------------------------
# HEARTBEAT LOOP
# ---------------------------

def heartbeat():
    while True:
        scan_and_register()
        time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=heartbeat, daemon=True).start()

    while True:
        time.sleep(1)
