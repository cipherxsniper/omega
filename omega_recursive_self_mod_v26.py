import os
import importlib.util
import threading
import time
import queue

class OmegaRecursiveSelfModV26:
    def __init__(self, root="."):
        self.root = root
        self.modules = {}
        self.bus = queue.Queue()
        self.running = False
        self.step = 0

    # -------------------------
    # DISCOVER ALL BRAINS
    # -------------------------
    def discover_modules(self):
        discovered = []

        for root, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".py") and not f.startswith("__"):
                    path = os.path.join(root, f)
                    discovered.append(path)

        return discovered

    # -------------------------
    # LOAD MODULE DYNAMICALLY
    # -------------------------
    def load_module(self, path):
        name = path.replace("/", ".").replace(".py", "")

        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.modules[name] = module
        return module

    # -------------------------
    # INIT ALL MODULES
    # -------------------------
    def init_modules(self):
        paths = self.discover_modules()

        for p in paths:
            try:
                self.load_module(p)
            except Exception as e:
                print(f"[LOAD ERROR] {p}: {e}")

    # -------------------------
    # MESSAGE BUS
    # -------------------------
    def publish(self, msg):
        self.bus.put(msg)

    def subscribe_loop(self):
        while self.running:
            try:
                msg = self.bus.get(timeout=1)
                self.dispatch(msg)
            except:
                pass

    # -------------------------
    # MODULE COMMUNICATION
    # -------------------------
    def dispatch(self, msg):
        for name, module in self.modules.items():
            if hasattr(module, "on_message"):
                try:
                    module.on_message(msg, self)
                except:
                    pass

    # -------------------------
    # RECURSIVE SELF MODIFICATION
    # -------------------------
    def self_modify(self):
        for name, module in self.modules.items():
            if hasattr(module, "self_adjust"):
                try:
                    module.self_adjust(self)
                except:
                    pass

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self):
        self.running = True
        self.init_modules()

        threading.Thread(target=self.subscribe_loop, daemon=True).start()

        print("[V26] RECURSIVE SELF-MODIFICATION ENGINE ONLINE")

        while self.running:
            self.step += 1

            self.publish({
                "step": self.step,
                "type": "heartbeat"
            })

            self.self_modify()

            time.sleep(0.2)
