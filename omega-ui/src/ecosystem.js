// 🌱 ECOSYSTEM SYSTEM (competition + survival pressure)

export function updateEcosystems(ecosystems) {

  let next = [];

  ecosystems.forEach(e => {

    // ⚔️ natural decay
    e.energy *= 0.995;

    // 🧬 population effect
    e.energy += (e.particles || 1) * 0.0008;

    // 🌱 growth stabilizes ecosystem
    if (e.particles > 8) {
      e.energy += 0.002;
    }

    e.age = (e.age || 0) + 1;

    // 💀 death condition
    if (e.energy > 0.1) {
      next.push(e);
    }
  });

  return next;
}

// 🌱 assign particle → ecosystem
export function assignEcosystem(p, ecosystems) {

  let target = null;

  for (let e of ecosystems) {
    const dx = e.x - p.x;
    const dy = e.y - p.y;

    if (Math.sqrt(dx*dx + dy*dy) < 0.15) {
      target = e;
      break;
    }
  }

  if (!target) {
    target = {
      id: Math.random(),
      x: p.x,
      y: p.y,
      particles: 0,
      energy: 1,
      age: 0
    };
    ecosystems.push(target);
  }

  target.particles++;
  return target.id;
}
