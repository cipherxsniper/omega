console.log("🧠 Omega v3 Swarm Kernel Booting...");

const swarm = require("./swarm/init");

setInterval(() => {
  swarm.tick();

  const snapshot = swarm.snapshot();

  console.log("🧬 SWARM STATE:");

  Object.values(snapshot).forEach(n => {
    console.log(
      `- ${n.id} | energy: ${n.energy.toFixed(2)} | links: ${n.links.length}`
    );
  });

}, 2000);
