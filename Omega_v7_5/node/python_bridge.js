const fs = require("fs");
const bus = require("../core/event_bus");

const file = "../bus/python_signal.json";

setInterval(() => {
  if (fs.existsSync(file)) {
    const data = JSON.parse(fs.readFileSync(file));

    bus.emitEvent({
      type: "python_bridge_event",
      confidence: data.confidence,
      payload: data.payload
    });
  }
}, 300);
