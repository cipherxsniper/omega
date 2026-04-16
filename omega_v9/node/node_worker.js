const fs = require("fs");

function emit() {
  const msg = {
    node: "js_worker",
    type: "signal",
    confidence: Math.random(),
    payload: { value: Math.random() * 100 }
  };

  fs.writeFileSync("omega_v9_bus.json", JSON.stringify(msg));
}

setInterval(emit, 300);
