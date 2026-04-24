// 🌌 UNIVERSAL FORKING SYSTEM

export function updateUniverses(ecosystems, universes) {

  const next = [...universes];

  ecosystems.forEach(e => {

    // 🌌 fork condition (stable + large ecosystem)
    if (e.energy > 1.2 && e.particles > 10 && !e.forked) {

      next.push({
        id: Math.random().toString(36).slice(2),
        parent: e.id,
        x: e.x,
        y: e.y,

        // ⚛️ unique physics per universe
        physics: {
          gravity: (Math.random() - 0.5) * 0.003,
          friction: 0.95 + Math.random() * 0.05,
          mutation: Math.random() * 0.02
        },

        stability: 1,
        age: 0
      });

      e.forked = true;
    }
  });

  return next;
}

// 🌌 universe visual mapping
export function renderUniverses(ctx, universes, canvas) {

  universes.forEach(u => {

    const x = (u.x || 0.5) * canvas.width;
    const y = (u.y || 0.5) * canvas.height;

    ctx.strokeStyle = "rgba(150,0,255,0.4)";
    ctx.beginPath();
    ctx.arc(x, y, 80, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = "purple";
    ctx.fillText(
      "UNI-" + u.id.slice(0,5),
      x + 10,
      y + 10
    );
  });
}
