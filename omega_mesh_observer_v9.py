from omega_cognitive_mesh_v9 import MESH

def on_reinforcement(event):
    print("[Ω MESH REINFORCEMENT]", event)

def on_tick(event):
    if event["load"] > 0.85:
        print("[Ω ALERT] overload detected:", event["node"])

MESH.subscribe("node.reinforcement", on_reinforcement)
MESH.subscribe("node.tick", on_tick)

print("[Ω] Cognitive Observer Online")
