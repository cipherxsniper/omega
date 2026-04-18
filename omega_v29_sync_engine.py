from omega_v29_global_memory_mesh import write_memory
from omega_v29_node_bus import emit

def sync(node, message):
    concepts = message.lower().split()

    for c in concepts:
        write_memory(node, c)

    emit(node, "memory_update", {
        "message": message,
        "concepts": concepts
    })

    return f"🧠 {node} synced {len(concepts)} concepts into global mesh"
