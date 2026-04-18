import os
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

ROOT = os.path.expanduser("~/Omega")

STATE = {
    "status": "booting",
    "nodes": [],
    "timestamp": 0
}

# ---------------------------
# NODE SCAN (SAFE)
# ---------------------------

def scan_nodes():
    nodes = []
    for r, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".py"):
                nodes.append(os.path.join(r, f))
    return nodes

# ---------------------------
# UPDATE STATE LOOP
# ---------------------------

def update_state():
    while True:
        STATE["nodes"] = scan_nodes()
        STATE["timestamp"] = time.time()
        STATE["status"] = "running"
        time.sleep(5)

# ---------------------------
# HTTP HANDLER
# ---------------------------

class Handler(BaseHTTPRequestHandler):

    def _send(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/status":
            self._send({
                "status": STATE["status"],
                "total_nodes": len(STATE["nodes"]),
                "message": "Omega cluster is active",
                "time": STATE["timestamp"]
            })

        elif self.path == "/nodes":
            self._send({
                "nodes": STATE["nodes"][:50]
            })

        else:
            self._send({"error": "unknown route"})

# ---------------------------
# START SERVER
# ---------------------------

def start_server():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("🧠 Omega v51 Cluster API running on port 8080")
    server.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=update_state, daemon=True)
    t.start()

    start_server()
