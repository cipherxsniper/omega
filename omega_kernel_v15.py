import time
import traceback
import importlib
import random

MODULES = {
    "ml": "omega_ml_core_v12",
    "swarm": "omega_swarm_v30_synchronized_evolution",
    "memory": "omega_memory_federation_v28"
}

class SafeModule:
    def __init__(self, name, module_path):
        self.name = name
        self.module_path = module_path
        self.module = None
        self.fail_count = 0
        self.last_restart = 0

    def start(self):
        try:
            self.module = importlib.import_module(self.module_path)
            print(f"[V15] Started module: {self.name}")
        except Exception as e:
            print(f"[V15] Failed to start {self.name}: {e}")

    def tick(self):
        try:
            if hasattr(self.module, "tick"):
                self.module.tick()
            else:
                # fallback heartbeat simulation
                print(f"[V15] {self.name} alive | heartbeat")
        except Exception as e:
            self.fail_count += 1
            print(f"[V15 ERROR] {self.name}: {e}")

            if self.fail_count >= 3:
                now = time.time()
                if now - self.last_restart > 5:  # cooldown prevents crash loop
                    print(f"[V15] restarting {self.name} safely...")
                    self.last_restart = now
                    self.fail_count = 0
                    self.start()


class OmegaKernelV15:
    def __init__(self):
        self.modules = {
            name: SafeModule(name, path)
            for name, path in MODULES.items()
        }

    def boot(self):
        print("[V15] AUTONOMOUS CONTROL KERNEL ONLINE")

        for m in self.modules.values():
            m.start()

        tick = 0

        while True:
            tick += 1
            print(f"[V15] tick {tick} | modules={len(self.modules)}")

            for m in self.modules.values():
                m.tick()

            time.sleep(1)


if __name__ == "__main__":
    OmegaKernelV15().boot()
