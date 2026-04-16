import socket
import json
import time
import sys

HOST = "127.0.0.1"
PORT = 5050

service = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    msg = {
        "service": service,
        "type": "heartbeat",
        "ts": time.time()
    }

    sock.send(json.dumps(msg).encode())
    time.sleep(2)
