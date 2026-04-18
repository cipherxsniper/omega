import socket
import threading
import json
import os
import time
import ast
from collections import defaultdict

HOST = "127.0.0.1"
PORT = 5051

NODE_REGISTRY = {}
DEPENDENCY_GRAPH = defaultdict(list)

# ---------------------------
# IPC BUS
# ---------------------------

def handle_node(conn, addr):
    NODE_REGISTRY[str(addr)] = {
        "status": "online",
        "last_seen": time.time()
    }

    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break

            msg = json.loads(data)
            process_message(msg)

        except:
            break

    NODE_REGISTRY[str(addr)]["status"] = "offline"
    conn.close()

# ---------------------------
# MESSAGE PROCESSOR
# ---------------------------

def process_message(msg):
    print("\n📡 IPC MESSAGE")
    print(f"FROM: {msg.get('from')}")
    print(f"TO: {msg.get('to')}")
    print(f"TYPE: {msg.get('type')}")
    print(f"DATA: {msg.get('data')}")

# ---------------------------
# BUS SERVER
# ---------------------------

def start_bus():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(100)

    print("🧠 Omega v41 IPC Bus Running")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_node, args=(conn, addr), daemon=True).start()

# ---------------------------
# DEPENDENCY GRAPH BUILDER
# ---------------------------

def extract_imports(file_path):
    try:
        with open(file_path, "r", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=file_path)

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return imports
    except:
        return []

def build_graph(root):
    for r, _, files in os.walk(root):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(r, f)
                deps = extract_imports(path)
                DEPENDENCY_GRAPH[path] = deps

# ---------------------------
# HUMAN-READABLE OUTPUT
# ---------------------------

def render_graph():
    print("\n🔗 DEPENDENCY GRAPH (READABLE VIEW)\n")

    for node, deps in list(DEPENDENCY_GRAPH.items())[:20]:
        print(f"📦 {os.path.basename(node)}")
        for d in deps[:5]:
            print(f"   └── imports: {d}")

# ---------------------------
# NODE HEARTBEAT SIMULATION
# ---------------------------

def heartbeat_monitor():
    while True:
        print("\n🧾 NODE STATUS")
        for node, info in NODE_REGISTRY.items():
            print(f"{node} → {info['status']}")
        time.sleep(5)

# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":
    threading.Thread(target=start_bus, daemon=True).start()

    time.sleep(1)

    build_graph(os.path.expanduser("~/Omega"))

    threading.Thread(target=heartbeat_monitor, daemon=True).start()

    while True:
        render_graph()
        time.sleep(10)
