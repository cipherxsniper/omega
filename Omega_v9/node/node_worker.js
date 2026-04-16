const fs = require("fs");

setInterval(() => {
  const msg = {
    node: "js_worker",
    confidence: Math.random(),
    payload: { value: Math.random() * 100 }
  };

  fs.writeFileSync("omega_v9_bus.json", JSON.stringify(msg));
}, 300);
