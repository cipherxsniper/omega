import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 5051

ROUTES = {}

# ---------------------------
# REGISTER ROUTE
# ---------------------------

def register_route(node_id, conn):
    ROUTES[node_id] = conn

# ---------------------------
# ROUTE MESSAGE
# ---------------------------

def route_message(msg):
    target = msg.get("to")

    if target == "broadcast":
        for c in ROUTES.values():
            try:
                c.send(json.dumps(msg).encode())
            except:
                pass
        return

    if target in ROUTES:
        try:
            ROUTES[target].send(json.dumps(msg).encode())
        except:
            pass

# ---------------------------
# HANDLE NODE
# ---------------------------

def handle(conn, addr):
    node_id = str(addr)
    register_route(node_id, conn)

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break

            msg = json.loads(data)
            route_message(msg)

        except:
            break

    conn.close()
    ROUTES.pop(node_id, None)

# ---------------------------
# SERVER
# ---------------------------

def start():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(100)

    print("🧠 v46 ROUTER ONLINE")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start()
