import json
import os

MEMORY_FILE = "omega_v29_global_memory.json"

def load():
    if not os.path.exists(MEMORY_FILE):
        return {"nodes": {}, "global_memory": [], "concept_graph": {}}
    return json.load(open(MEMORY_FILE))

def save(mem):
    json.dump(mem, open(MEMORY_FILE, "w"))

def write_memory(node, concept):
    mem = load()

    if node not in mem["nodes"]:
        mem["nodes"][node] = []

    mem["nodes"][node].append(concept)
    mem["global_memory"].append({"node": node, "concept": concept})

    mem["concept_graph"][concept] = mem["concept_graph"].get(concept, 0) + 1

    save(mem)
    return mem
