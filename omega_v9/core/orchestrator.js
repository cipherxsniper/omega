const fs = require("fs");

let memory = [];

console.log("🧠 Omega v9 Swarm ACTIVE");

setInterval(() => {
  try {
    const data = JSON.parse(fs.readFileSync("omega_v9_bus.json"));

    memory.push(data);

    if (memory.length > 20) memory.shift();

    const avg = memory.reduce((a, b) => a + (b.confidence || 0), 0) / memory.length;

    console.log("📊 Swarm Confidence:", avg.toFixed(4));

  } catch (e) {}
}, 200);
