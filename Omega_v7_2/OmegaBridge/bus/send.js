const fs = require("fs");
const path = require("path");

function sendOmegaMessage(msg) {
  const file = path.join(__dirname, "omega_message.json");

  msg.timestamp = Date.now();

  fs.writeFileSync(file, JSON.stringify(msg, null, 2));
  console.log("📤 Node sent:", msg.type);
}

// example usage
sendOmegaMessage({
  type: "node_signal",
  from: "node_core",
  to: "python_core",
  payload: { action: "learn", value: Math.random() }
});
