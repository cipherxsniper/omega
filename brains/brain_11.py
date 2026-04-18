from core.omega_bus_v29 import BUS, emit

memory_strength = 0

def step():

    global memory_strength

    signals = len(BUS["signals"])

    memory_strength += signals * 0.001

    emit("brain_11", {
        "memory": memory_strength
    })
