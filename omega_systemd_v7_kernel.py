import os
import time
import socket
import json
import threading
import subprocess
from collections import defaultdict, deque

LOG = lambda x: print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} [V7] {x}")

# -----------------------------
# SERVICE CONTRACT LAYER
# -----------------------------
class ServiceContract:
    def __init__(self, name):
        self.name = name

    def preflight(self):
        return os.path.exists(self.name)

    def validate_runtime(self, proc):
        return proc.poll() is None


# -----------------------------
# IPC BUS (LIGHTWEIGHT SOCKET)
# -----------------------------
class IPCBus:
    def __init__(self, port=5050):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listeners = []

    def send(self, msg):
        data = json.dumps(msg).encode()
        self.sock.sendto(data, ("127.0.0.1", self.port))

    def listen(self):
        self.sock.bind(("0.0.0.0", self.port))
        LOG("IPC BUS ONLINE")

        while True:
            data, _ = self.sock.recvfrom(4096)
            msg = json.loads(data.decode())
            for cb in self.listeners:
                cb(msg)

    def register(self, cb):
        self.listeners.append(cb)


# -----------------------------
# DAG RESOLVER
# -----------------------------
def build_dag(services):
    graph = defaultdict(list)
    indegree = defaultdict(int)

    for s in services:
        indegree[s] = 0

    for i in range(len(services) - 1):
        a, b = services[i], services[i + 1]
        graph[a].append(b)
        indegree[b] += 1

    queue = deque([n for n in services if indegree[n] == 0])
    order = []

    while queue:
        n = queue.popleft()
        order.append(n)

        for m in graph[n]:
            indegree[m] -= 1
            if indegree[m] == 0:
                queue.append(m)

    return order


# -----------------------------
# SWARM CONSENSUS (SIMPLE)
# -----------------------------
class SwarmConsensus:
    def __init__(self):
        self.heartbeats = {}

    def ping(self, service):
        self.heartbeats[service] = time.time()

    def alive(self, service):
        return time.time() - self.heartbeats.get(service, 0) < 5


# -----------------------------
# CRASH CLASSIFIER
# -----------------------------
def classify_crash(proc):
    if proc is None:
        return "NO_PROC"

    code = proc.poll()
    if code is None:
        return "RUNNING"
    if code == 0:
        return "CLEAN_EXIT"
    if code < 0:
        return "SIGNALED_KILL"
    return "NON_ZERO_EXIT"


# -----------------------------
# SYSTEMD V7 KERNEL
# -----------------------------
class OmegaSystemD7:

    def __init__(self, services):
        self.services = services
        self.order = build_dag(services)
        self.processes = {}
        self.bus = IPCBus()
        self.swarm = SwarmConsensus()

    def start_service(self, s):
        contract = ServiceContract(s)

        if not contract.preflight():
            LOG(f"BLOCK → missing {s}")
            return

        LOG(f"START → {s}")

        proc = subprocess.Popen(
            ["python", s],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.processes[s] = proc
        self.swarm.ping(s)

    def monitor(self):
        while True:
            time.sleep(2)

            for s, p in list(self.processes.items()):
                state = classify_crash(p)

                if state == "RUNNING":
                    self.swarm.ping(s)
                    continue

                LOG(f"STATE → {s} = {state}")

                if state != "RUNNING":
                    LOG(f"RESTART → {s}")
                    self.start_service(s)

    def boot(self):
        LOG("BOOT START")
        LOG(f"ORDER: {self.order}")

        for s in self.order:
            self.start_service(s)

        LOG("BOOT COMPLETE")

        t = threading.Thread(target=self.bus.listen, daemon=True)
        t.start()

        self.monitor()


# -----------------------------
# ENTRY
# -----------------------------
if __name__ == "__main__":
    services = [
        "omega_kernel_v47.py",
        "omega_process_supervisor_v2.py",
        "omega_event_bus_v12.py",
        "omega_execution_engine_v7.py",
        "omega_meta_brain_v10.py",
        "omega_router_v37.py"
    ]

    OmegaSystemD7(services).boot()
