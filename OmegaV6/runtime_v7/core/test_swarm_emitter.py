import socket
import time
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    event = {
        "type": "heartbeat",
        "content": "alive",
        "node_id": "emitter-1",
        "timestamp": time.time()
    }

    sock.sendto(
        json.dumps(event).encode("utf-8"),
        ("127.0.0.1", 6100)
    )

    print("[EMITTER] sent heartbeat")
    time.sleep(2)
