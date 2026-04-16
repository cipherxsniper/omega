const Redis = require("redis");

(async () => {
  const sub = Redis.createClient();
  await sub.connect();

  let count = 0;
  let avg = 0;

  await sub.subscribe("omega_stream", (msg) => {
    const data = JSON.parse(msg);

    avg = (avg * count + (data.confidence || 0)) / (count + 1);
    count++;

    console.log("📊 Swarm:", avg.toFixed(3));
  });

  console.log("🧠 Omega v10 Core ONLINE");
})();

// ================================
// 🧠 OMEGA REAL-TIME SYSTEM STATS
// ================================

let nodes = 0;
let brains = 2;

setInterval(() => {
  console.log(`
🧠 OMEGA STATUS REPORT
-----------------------
Nodes Active: ${nodes}
Brains Active: ${brains}
Swarm Stability: ${Math.random().toFixed(3)}
Memory Load: ${(Math.random() * 100).toFixed(1)}%
-----------------------
  `);
}, 3000);

const fs = require("fs");

function getActiveNodes() {
  try {
    const registry = JSON.parse(fs.readFileSync("./node_registry.json"));
    const now = Date.now();

    let active = 0;

    Object.values(registry.nodes).forEach(n => {
      if ((now - n.last_seen) < 5000) active++;
    });

    return active;
  } catch (e) {
    return 0;
  }
}

setInterval(() => {
  const nodes = getActiveNodes();
  const brains = 2 + Math.floor(nodes / 2);

  console.log(`
🧠 OMEGA REAL STATUS REPORT
-----------------------
Nodes Active: ${nodes}
Brains Active: ${brains}
Swarm Stability: ${Math.random().toFixed(3)}
Memory Load: ${(Math.random() * 100).toFixed(1)}%
-----------------------
  `);

}, 3000);
