const bus = require("../core/event_bus");

function generateSignal(id) {
  return {
    type: "node_signal",
    node: id,
    confidence: Math.random(),
    payload: {
      value: Math.random() * 100
    }
  };
}

setInterval(() => {
  const signal = generateSignal("node_js_" + Math.floor(Math.random() * 10));
  bus.emitEvent(signal);
}, 500);
