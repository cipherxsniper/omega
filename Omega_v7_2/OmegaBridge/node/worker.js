const fs = require("fs");

function generateSignal() {
  return {
    type: "node_worker_signal",
    from: "worker_node",
    to: "python_core",
    payload: {
      action: "learn",
      value: Math.random()
    },
    timestamp: Date.now()
  };
}

setInterval(() => {
  const msg = generateSignal();

  fs.writeFileSync("../bus/omega_message.json", JSON.stringify(msg, null, 2));
  console.log("⚙️ Worker generated signal");
}, 3000);
