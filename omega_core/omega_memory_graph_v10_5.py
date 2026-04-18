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
