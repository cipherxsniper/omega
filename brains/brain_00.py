import random
from core.omega_bus_v29 import BUS, emit, write

particles = [{"x": random.randint(0,50), "y": random.randint(0,50)} for _ in range(30)]

def step():

    for p in particles:
        p["x"] += random.randint(-1,1)
        p["y"] += random.randint(-1,1)

    write("swarm_density", len(particles))
    emit("brain_00", {"particles": len(particles)})
