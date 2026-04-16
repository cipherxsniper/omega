from runtime_v7.core.omega_memory_graph_v2 import get_memory

mem = get_memory()

def enhanced_store(event):
    key = f"{event.get('type')}"

    if key not in mem.graph:
        mem.graph[key] = {
            "count": 0,
            "last_seen": 0,
            "patterns": []
        }

    mem.graph[key]["count"] += 1
    mem.graph[key]["last_seen"] = event.get("timestamp", 0)

    # detect simple pattern
    if mem.graph[key]["count"] % 5 == 0:
        mem.graph[key]["patterns"].append("repeating_signal")

    mem.save()

def summary():
    return {
        "event_types": len(mem.graph),
        "total_patterns": sum(len(v["patterns"]) for v in mem.graph.values())
    }

mem.enhanced_store = enhanced_store
mem.summary = summary

print("[OMEGA MEMORY PATCH] ACTIVE")
