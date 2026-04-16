const fs = require("fs");

let memory = [];

console.log("🧠 Omega v9 ONLINE");

setInterval(() => {
  try {
    const data = JSON.parse(fs.readFileSync("omega_v9_bus.json"));
    memory.push(data);

    const avg = memory.reduce((a,b)=>a+(b.confidence||0),0)/memory.length;

    console.log("📊 Swarm:", avg.toFixed(3));
  } catch (e) {}
}, 200);
