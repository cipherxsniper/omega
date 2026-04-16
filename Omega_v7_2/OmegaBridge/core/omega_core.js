console.log("🧠 Omega Swarm Core Active");

const fs = require("fs");

let memory = [];

setInterval(() => {
  const file = "../bus/omega_message.json";

  if (!fs.existsSync(file)) return;

  const msg = JSON.parse(fs.readFileSync(file));

  memory.push(msg);

  if (memory.length > 20) memory.shift();

  const avg = memory.reduce((a, b) => {
    return a + (b.payload?.value || 0);
  }, 0) / memory.length;

  console.log("📊 Omega Memory Avg:", avg.toFixed(4));

}, 2000);
