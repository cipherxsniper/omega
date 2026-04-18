import json
import os

MEMORY_FILE = "omega_belief_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"beliefs": {}, "history": []}
    return json.load(open(MEMORY_FILE))

def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w"))

def update_belief(mem, concept):
    mem["beliefs"][concept] = mem["beliefs"].get(concept, 0) + 1

def get_dominant_belief(mem):
    if not mem["beliefs"]:
        return None
    return max(mem["beliefs"], key=mem["beliefs"].get)
