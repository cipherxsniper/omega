import os
import importlib.util
import time
import random

class OmegaSelfReflectiveKernelV63:
    def __init__(self, root="."):
        self.root = root
        self.modules = {}
        self.active_brains = []
        self.state = {
            "tick": 0,
            "signals": [],
            "executed": []
        }

    # 🧠 scan system (your ls files become cognition nodes)
    def scan_brains(self):
        files = [f for f in os.listdir(self.root) if f.endswith(".py")]

        self.modules = {}
        for f in files:
            name = f.replace(".py", "")
            self.modules[name] = f

    # ⚡ dynamic loader
    def load_module(self, name):
        path = self.modules[name]

        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        return mod

    # 🧠 decide what runs
    def select_brains(self):
        keys = list(self.modules.keys())

        # keep kernel stable
        priority = [k for k in keys if "kernel" in k or "brain" in k]

        chosen = random.sample(keys, min(5, len(keys)))
        self.active_brains = list(set(priority + chosen))

    # ⚡ execute cognition
    def tick(self):
        self.state["tick"] += 1
        self.scan_brains()
        self.select_brains()

        print(f"\n[Ω-v6.3] tick={self.state['tick']} active_brains={len(self.active_brains)}")

        for b in self.active_brains:
            try:
                mod = self.load_module(b)

                if hasattr(mod, "step"):
                    result = mod.step(self.state)
                    self.state["signals"].append((b, result))

                self.state["executed"].append(b)

            except Exception as e:
                self.state["signals"].append((b, f"ERROR: {str(e)}"))

        time.sleep(0.2)

    def run(self):
        while True:
            self.tick()


if __name__ == "__main__":
    OmegaSelfReflectiveKernelV63().run()
