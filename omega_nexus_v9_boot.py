import subprocess
import time
import os

print("[Ω NEXUS v9 BOOT] Initializing ecosystem...\n")

# ----------------------------
# PHASE 1: CORE MESH
# ----------------------------
core = subprocess.Popen(["python3", "omega_neural_bus_v9.py"])
time.sleep(1)

mesh = subprocess.Popen(["python3", "omega_cognitive_mesh_v9.py"])
time.sleep(1)

# ----------------------------
# PHASE 2: CHAT INTERFACE
# ----------------------------
chat = subprocess.Popen(["python3", "omega_chat_assistant_v9_bus.py"])
time.sleep(1)

# ----------------------------
# PHASE 3: OBSERVER
# ----------------------------
observer = subprocess.Popen(["python3", "omega_swarm_balancer_v9_bus.py"])
time.sleep(1)

# ----------------------------
# PHASE 4: NODE BATCH (controlled scaling)
# ----------------------------
nodes = []
node_files = [
    ("node_1", "brain"),
    ("node_2", "kernel"),
    ("node_3", "memory"),
    ("node_4", "learning"),
]

for n, role in node_files:
    p = subprocess.Popen([
        "python3",
        "omega_mesh_node_v9.py",
        n,
        role
    ])
    nodes.append(p)
    time.sleep(0.5)

print("\n[Ω NEXUS v9 ONLINE]")
print("[Ω] Bus running")
print("[Ω] Mesh active")
print("[Ω] Chat online")
print("[Ω] Nodes deployed:", len(nodes))

# keep alive
while True:
    time.sleep(10)
