import os
import psutil
import time

class OmegaMetaControllerV6_3:

    def __init__(self):
        self.registry = {}  # pid → process info
        self.node_map = {}
        self.attention_state = {}

    # -------------------------
    # EXECUTION REGISTRY
    # -------------------------
    def scan_processes(self):
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if "python" in p.info['name']:
                    processes.append(p.info)
            except:
                continue
        return processes

    def update_registry(self):
        procs = self.scan_processes()
        self.registry = {p['pid']: p for p in procs}

    # -------------------------
    # NODE DISCOVERY (FILESYSTEM → NODES)
    # -------------------------
    def scan_nodes(self, base="~/Omega"):
        base = os.path.expanduser(base)
        nodes = []

        for root, dirs, files in os.walk(base):
            for f in files:
                if f.endswith(".py"):
                    nodes.append(os.path.join(root, f))

        return nodes

    def update_nodes(self):
        nodes = self.scan_nodes()
        for n in nodes:
            self.node_map[n] = self.node_map.get(n, 0.5)

    # -------------------------
    # ATTENTION DISTRIBUTION
    # -------------------------
    def compute_attention(self):
        total = len(self.node_map) + 1
        self.attention_state = {
            k: (v / total)
            for k, v in self.node_map.items()
        }

    # -------------------------
    # CONFLICT DETECTION
    # -------------------------
    def detect_overload(self):
        return len(self.registry) > 50

    # -------------------------
    # MAIN TICK
    # -------------------------
    def tick(self):
        self.update_registry()
        self.update_nodes()
        self.compute_attention()

        return {
            "active_processes": len(self.registry),
            "total_nodes": len(self.node_map),
            "overload": self.detect_overload(),
            "top_attention": sorted(
                self.attention_state.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

    # -------------------------
    # SAFE RUN LOOP
    # -------------------------
    def run(self, delay=2.0):
        while True:
            state = self.tick()
            print(state)
            time.sleep(delay)


if __name__ == "__main__":
    OmegaMetaControllerV6_3().run()
