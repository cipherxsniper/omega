from core.omega_bus_v29 import BUS, emit

def step():

    density = BUS["state"].get("swarm_density", 0)

    structure = density * 0.5

    emit("brain_22", {
        "structure": structure
    })
