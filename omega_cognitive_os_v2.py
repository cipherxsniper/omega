import time
import random
import json
import os
import copy


class OmegaCognitiveOSV2:

    def __init__(self, memory_file="omega_memory_mesh.json"):
        self.memory_file = memory_file
        self.state = self._boot()
        self.load_memory()

    # ---------------------------
    # BOOT
    # ---------------------------
    def _boot(self):
        return {
            "agents": {
                "brain_0": 50.0,
                "brain_1": 50.0,
                "brain_2": 50.0,
                "brain_3": 50.0
            },
            "strongest": "brain_0",
            "status": "booting",
            "timestamp": time.time(),
            "nodes": {},
            "memory_mesh": {
                "global_memory": [],
                "node_memory": {}
            },
            "events": [],
            "meta": {
                "version": "v2",
                "cycle": 0,
                "node_count": 0,
                "self_heal_count": 0
            }
        }

    # ---------------------------
    # SELF-HEAL
    # ---------------------------
    def heal(self):
        s = self.state

        if "agents" not in s:
            s["agents"] = {}

        if "nodes" not in s:
            s["nodes"] = {}

        if "memory_mesh" not in s:
            s["memory_mesh"] = {"global_memory": [], "node_memory": {}}

        if "events" not in s:
            s["events"] = []

        if "meta" not in s:
            s["meta"] = {"version": "v2", "cycle": 0, "node_count": 0, "self_heal_count": 0}

        s["meta"]["self_heal_count"] += 1
        return s

    # ---------------------------
    # NODE EVOLUTION ENGINE
    # ---------------------------
    def evolve_nodes(self):
        s = self.state

        # decay old nodes
        for nid in list(s["nodes"].keys()):
            node = s["nodes"][nid]
            node["age"] += 1
            node["power"] *= 0.99

            # prune weak nodes
            if node["power"] < 10:
                s["events"].append({"type": "NODE_PRUNED", "node": nid})
                del s["nodes"][nid]

        # spawn new node from strongest brain
        strongest = max(s["agents"], key=s["agents"].get)

        if len(s["nodes"]) < 6:
            nid = f"node_{len(s['nodes'])}_{int(time.time())}"

            s["nodes"][nid] = {
                "type": "brain_extension",
                "power": s["agents"][strongest] * 0.1,
                "age": 0,
                "connections": [strongest],
                "memory_ref": f"mem_{nid}"
            }

            s["events"].append({
                "type": "NODE_SPAWNED",
                "node": nid,
                "from": strongest
            })

    # ---------------------------
    # MEMORY MESH
    # ---------------------------
    def write_memory(self, event):
        self.state["memory_mesh"]["global_memory"].append(event)

        # persist to disk
        with open(self.memory_file, "w") as f:
            json.dump(self.state["memory_mesh"], f)

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    self.state["memory_mesh"] = json.load(f)
            except:
                pass

    # ---------------------------
    # CORE STEP (ONLY ENTRYPOINT)
    # ---------------------------
    def step(self):
        s = self.state
        s = self.heal()

        # update brains
        for b in s["agents"]:
            s["agents"][b] += random.uniform(-3, 3)

        # strongest brain
        s["strongest"] = max(s["agents"], key=s["agents"].get)

        # node evolution
        self.evolve_nodes()

        # memory logging
        event = {
            "cycle": s["meta"]["cycle"],
            "strongest": s["strongest"],
            "timestamp": time.time()
        }

        self.write_memory(event)

        s["events"].append(event)

        # meta update
        s["meta"]["cycle"] += 1
        s["meta"]["node_count"] = len(s["nodes"])
        s["timestamp"] = time.time()
        s["status"] = "running"

        return copy.deepcopy(s)
