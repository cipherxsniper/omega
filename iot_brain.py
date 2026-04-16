import socket
import time
import json
import random

HOST = "127.0.0.1"
PORT = 5555

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

sock = connect()

while True:
    data = {
        "brain": "iot_sensor",
        "temperature": random.randint(60, 100),
        "movement": random.choice([0, 1])
    }

    sock.sendall(json.dumps(data).encode())
    time.sleep(1)

# OPTIMIZED BY v29 ENGINE
