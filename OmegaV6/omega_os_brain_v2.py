import os
import time

from omega_os_registry_v2 import OmegaOSRegistryV2
from omega_execution_engine_v2 import OmegaExecutionEngineV2
from omega_health_monitor_v2 import OmegaHealthMonitorV2

class OmegaOSBrainV2:
    def __init__(self):
        self.registry = OmegaOSRegistryV2()
        self.engine = OmegaExecutionEngineV2()
        self.health = OmegaHealthMonitorV2()

        self.max_active = 25

    def boot(self):
        print("\n🧠 OMEGA OS BRAIN v2 (SYSTEMD REPLACEMENT)\n")

        modules = self.scan_modules()

        for m in modules:
            self.registry.register(m)
            self.engine.start(m)

        self.loop()

    def scan_modules(self):
        base = os.path.expanduser("~/Omega/OmegaV6")
        return [f for f in os.listdir(base) if f.endswith(".py")][:self.max_active]

    def loop(self):
        while True:
            time.sleep(3)

            for name, meta in list(self.registry.state["services"].items()):
                if not self.health.heartbeat_ok(meta["last_seen"]):
                    action = self.health.report_failure(name)

                    if action == "BLACKLIST":
                        print(f"🛑 BLACKLISTED: {name}")
                        continue

                    elif action == "COOLDOWN":
                        print(f"⏳ COOLDOWN: {name}")
                        continue

                    print(f"♻️ RESTART: {name}")
                    self.engine.start(name)

if __name__ == "__main__":
    OmegaOSBrainV2().boot()
