#!/bin/bash

echo "🧠 OMEGA v10.5 BOOTSTRAP INIT"

mkdir -p omega_core

# ---------------------------
# MEMORY GRAPH
# ---------------------------
cat > omega_core/omega_memory_graph_v10_5.py << 'PY'
# Shared memory graph (stable production core)

import json, os, time

FILE = "omega_state_v10_5.json"

def load():
    if os.path.exists(FILE):
        return json.load(open(FILE))
    return {"global": [], "nodes": {}}

def save(s):
    json.dump(s, open(FILE,"w"), indent=2)

class MemoryGraph:
    def __init__(self):
        self.s = load()

    def node(self,n):
        if n not in self.s["nodes"]:
            self.s["nodes"][n] = {
                "mem": [],
                "w": 0.5,
                "stability": 0.5,
                "influence": 0.5
            }
        return self.s["nodes"][n]

    def write(self,n,e,v=0.0):
        self.node(n)
        entry={"n":n,"e":e,"v":v,"t":time.time()}
        self.s["global"].append(entry)
        self.s["nodes"][n]["mem"].append(entry)
        self.s["global"]=self.s["global"][-300:]
        self.s["nodes"][n]["mem"]=self.s["nodes"][n]["mem"][-100:]
        save(self.s)
PY

# ---------------------------
# EVOLUTION ENGINE
# ---------------------------
cat > omega_core/omega_evolution_v10_5.py << 'PY'
def pressure(node):
    mem=len(node.get("mem",[]))/100
    stab=1-node.get("stability",0.5)
    inf=1-node.get("influence",0.5)
    return min(1,max(0, mem*0.4 + stab*0.4 + inf*0.2))

def state(p):
    if p>0.75: return "SPLIT"
    if p>0.5: return "ADAPT"
    if p>0.25: return "LEARN"
    return "STABLE"
PY

# ---------------------------
# CONTROL ROUTER
# ---------------------------
cat > omega_core/omega_router_v10_5.py << 'PY'
from omega_core.omega_memory_graph_v10_5 import MemoryGraph
from omega_core.omega_evolution_v10_5 import pressure, state

class Router:
    def __init__(self):
        self.m=MemoryGraph()

    def tick(self,nodes):
        out={}
        for n in nodes:
            node=self.m.node(n)
            p=pressure(node)
            s=state(p)

            self.m.write(n,s,p)

            out[n]={"pressure":p,"state":s}
        return out
PY

# ---------------------------
# BOOT FILE
# ---------------------------
cat > omega_core/run_omega_v10_5.py << 'PY'
from omega_core.omega_router_v10_5 import Router
import time

r=Router()
nodes=["memory","goal","attention","stability"]

print("🧠 OMEGA v10.5 RUNNING")

while True:
    print(r.tick(nodes))
    time.sleep(2)
PY

echo "✅ OMEGA v10.5 CORE BUILT"
echo "Run: python omega_core/run_omega_v10_5.py"
