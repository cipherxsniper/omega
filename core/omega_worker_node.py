# OMEGA WORKER NODE v2
# Distributed execution unit

import sys
import json
import socket
from omega_safe_import import safe_import

HOST = "127.0.0.1"


def handle_event(event):
    if event["type"] == "import_check":
        module = event["payload"]

        path = safe_import(module)

        return {
            "type": "import_result",
            "payload": {
                "module": module,
                "resolved": str(path) if path else None
            }
        }


def run(port):
    with socket.socket() as s:
        s.bind((HOST, port))
        s.listen()

        print(f"[Ω WORKER NODE] running on {port}")

        while True:
            conn, _ = s.accept()
            data = conn.recv(65536)

            try:
                event = json.loads(data.decode())
                response = handle_event(event)

                if response:
                    print(response)

            except Exception as e:
                print("[Ω WORKER ERROR]", str(e))


if __name__ == "__main__":
    port = int(sys.argv[1])
    run(port)
