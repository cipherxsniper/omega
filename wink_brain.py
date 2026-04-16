import socket
import time
import json
import random

HOST = "127.0.0.1"
PORT = 5555

BRAIN_ID = "wink_brain"

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

sock = connect()

ideas = [
    "inject_pattern",
    "random_boost",
    "disrupt_flow",
    "mutate_signal"
]

while True:
    idea = random.choice(ideas)

    event = {
        "brain": BRAIN_ID,
        "idea": idea,
        "entropy": random.random()
    }

    sock.sendall(json.dumps(event).encode())

    try:
        data = sock.recv(2048)
        print("[WINK RECEIVED]", data.decode())
    except:
        pass

    time.sleep(1.5)

# OPTIMIZED BY v29 ENGINE
