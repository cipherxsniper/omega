from system.omega_orchestrator_v4 import OmegaOrchestratorV4
import time

omega = OmegaOrchestratorV4()

print("🧠 OMEGA v12.2 SWARM MEMORY ONLINE")

while True:
    omega.run_cycle()
    time.sleep(2)
