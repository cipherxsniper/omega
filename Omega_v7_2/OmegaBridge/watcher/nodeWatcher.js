const fs = require("fs");

const file = "../bus/omega_message.json";

console.log("👁 Node watcher active...");

setInterval(() => {
  if (fs.existsSync(file)) {
    const data = JSON.parse(fs.readFileSync(file));

    if (data.learning_result) {
      console.log("🧠 Node learned from Python:", data.learning_result);

      // feedback loop (reinforcement signal)
      data.type = "reinforced_signal";
      data.payload.adjusted = data.learning_result.adjustment;

      fs.writeFileSync(file, JSON.stringify(data, null, 2));
    }
  }
}, 1000);
