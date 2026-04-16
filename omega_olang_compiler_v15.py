import time
import json
import random


# =========================
# 🧠 Ω-LANG COMPILER
# =========================
class OmegaLangCompiler:

    def __init__(self):

        self.queue = []
        self.node_graph = {}
        self.pending_changes = []

    # -------------------------
    # SUBMIT Ω-LANG INSTRUCTION
    # -------------------------
    def submit(self, instruction):

        self.queue.append(instruction)

    # -------------------------
    # PARSE Ω-LANG
    # -------------------------
    def parse(self, instruction):

        op = instruction.get("op")
        args = instruction.get("args", {})

        return op, args

    # -------------------------
    # EXECUTE SAFE OPERATION
    # -------------------------
    def execute(self, op, args):

        # =========================
        # CREATE NODE
        # =========================
        if op == "create_node":

            node_id = args["id"]

            self.node_graph[node_id] = {
                "strength": random.random(),
                "created": time.time(),
                "mutations": 0
            }

            print(f"[Ω-LANG] created node {node_id}")

        # =========================
        # MUTATE NODE
        # =========================
        elif op == "mutate_node":

            node_id = args["id"]

            if node_id in self.node_graph:

                node = self.node_graph[node_id]

                node["strength"] += random.uniform(-0.1, 0.1)
                node["mutations"] += 1

                print(f"[Ω-LANG] mutated node {node_id}")

        # =========================
        # LINK NODES
        # =========================
        elif op == "link_nodes":

            a = args["a"]
            b = args["b"]

            if a in self.node_graph and b in self.node_graph:

                self.pending_changes.append(("link", a, b))

                print(f"[Ω-LANG] queued link {a} → {b}")

        # =========================
        # EVOLVE SYSTEM
        # =========================
        elif op == "evolve":

            for node_id, node in self.node_graph.items():

                node["strength"] *= random.uniform(0.98, 1.02)

            print("[Ω-LANG] global evolution step executed")

    # -------------------------
    # COMPILE QUEUE
    # -------------------------
    def compile(self):

        while self.queue:

            instruction = self.queue.pop(0)

            op, args = self.parse(instruction)

            self.execute(op, args)

    # -------------------------
    # APPLY GRAPH CHANGES
    # -------------------------
    def commit(self):

        for change in self.pending_changes:

            if change[0] == "link":

                _, a, b = change

                self.node_graph[a]["link"] = b

        self.pending_changes = []

    # -------------------------
    # SYSTEM STEP
    # -------------------------
    def step(self):

        self.compile()
        self.commit()

    # -------------------------
    # DEBUG STATE
    # -------------------------
    def status(self):

        return {
            "nodes": len(self.node_graph),
            "sample": list(self.node_graph.keys())[:3]
        }


# =========================
# 🚀 DEMO
# =========================
if __name__ == "__main__":

    compiler = OmegaLangCompiler()

    print("[Ω-LANG v15] SELF-MODIFYING COMPILER ONLINE")

    # seed instructions
    compiler.submit({"op": "create_node", "args": {"id": "brain_0"}})
    compiler.submit({"op": "create_node", "args": {"id": "brain_1"}})
    compiler.submit({"op": "link_nodes", "args": {"a": "brain_0", "b": "brain_1"}})
    compiler.submit({"op": "evolve", "args": {}})

    tick = 0

    while True:

        tick += 1

        compiler.step()

        if tick % 5 == 0:
            print("[Ω-LANG STATUS]", compiler.status())

        time.sleep(0.5)
