from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79

from omega_memory_fusion_v721 import OmegaMemoryFusionV721
from omega_nodes_v721 import OmegaNodeV721
from omega_emergence_v721 import OmegaEmergenceV721

print("[Ω] booting v7.21 emergent cognition fusion layer...", flush=True)

layer = get_execution_layer()
kernel = OmegaKernelV79(layer)

memory = OmegaMemoryFusionV721()
emergence = OmegaEmergenceV721()

nodes = [
    OmegaNodeV721("A"),
    OmegaNodeV721("B"),
    OmegaNodeV721("C")
]

tick = 0

while True:

    raw = kernel.step(tick, {"drift": 40})

    # shared memory update
    memory.write("system_state", "active", raw)

    # nodes read from shared field
    for n in nodes:
        n.update(memory.field)

    # emergence detection
    patterns = emergence.detect_patterns(memory.field)
    summary = emergence.summarize(patterns)

    print(f"\n[Ω v7.21 | TICK {tick}]", flush=True)
    print(summary["summary"], flush=True)

    tick += 1
