from system.omega_shk_v4 import OmegaAdaptiveCompilerV4
import time
import random

class Engine:
    def step(self):
        agents = {
            "brain_0": random.uniform(40, 100),
            "brain_1": random.uniform(40, 100),
            "brain_2": random.uniform(40, 100),
            "brain_3": random.uniform(40, 100),
        }

        return {
            "agents": agents,
            "strongest": max(agents, key=agents.get),
            "status": "raw",
            "timestamp": time.time()
        }

engine = Engine()
kernel = OmegaAdaptiveCompilerV4(engine)

print("[Ω-SHK-4] Adaptive Intelligence Compiler ONLINE")

while True:
    frame = kernel.step()
    print(frame)
    time.sleep(0.5)
