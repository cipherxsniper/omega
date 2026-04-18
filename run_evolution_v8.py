import time
from omega.core.self_evolving_kernel_v8 import EvolutionKernelV8

kernel = EvolutionKernelV8()

print("🧬 Omega Evolution Kernel v8 ONLINE")

while True:
    result = kernel.run_cycle()

    print(
        f"[EVOLUTION] approved={result['approved']} "
        f"rejected={result['rejected']}"
    )

    time.sleep(5)
