from omega_cognitive_mesh_v9 import MESH

def chat(msg):
    event = {
        "node": "chat_interface",
        "load": 0.3,
        "message": msg
    }

    MESH.publish("node.tick", event)
    print("[Ω CHAT]", msg)

print("[Ω CHAT] Mesh-connected chat ready")
