// 🧬 SAFE PARTICLE MUTATION PROPOSAL SYSTEM

export function collectMutations(particles) {
  const mutations = [];

  for (const p of particles) {
    // only Box 3 particles can evolve brains
    if (p.box !== 3) continue;

    // probabilistic mutation proposal
    if (Math.random() < 0.01) {
      mutations.push({
        target: "box3.cloneRate",
        delta: (Math.random() - 0.5) * 0.01,
        reason: "adaptive_survival_signal",
        sourceParticle: p.id
      });
    }

    if (Math.random() < 0.005) {
      mutations.push({
        target: "box2.collapseRate",
        delta: (Math.random() - 0.5) * 0.005,
        reason: "quantum_stability_shift",
        sourceParticle: p.id
      });
    }

    if (Math.random() < 0.005) {
      mutations.push({
        target: "box1.friction",
        delta: (Math.random() - 0.5) * 0.003,
        reason: "reality_physics_drift",
        sourceParticle: p.id
      });
    }
  }

  return mutations;
}
