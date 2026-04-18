"""
Omega Swarm Influence Layer v12
Provides safe coupling for particle field modulation
"""

def apply_swarm_influence(particle):
    # lightweight stabilizing field bias
    particle.vx += (particle.vx * 0.001)
    particle.vy += (particle.vy * 0.001)
