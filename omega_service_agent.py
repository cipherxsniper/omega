import socket
import time
import os

PORT = 5050

def send_heartbeat():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    name = os.path.basename(__file__)

    while True:
        msg = f"{name}|{time.time()}"
        s.sendto(msg.encode(), ("127.0.0.1", PORT))
        time.sleep(2)

if __name__ == "__main__":
    send_heartbeat()
