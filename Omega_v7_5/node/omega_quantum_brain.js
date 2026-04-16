const bus = require("../core/event_bus");
const Memory = require("../memory/compression");
const Consensus = require("../core/consensus");

const memory = new Memory();
const consensus = new Consensus();

let buffer = [];

bus.on("event", (event) => {
  buffer.push(event);

  memory.add(event);

  if (buffer.length >= 5) {
    const decision = consensus.decide(buffer);

    console.log("⚡ CONSENSUS:", decision);

    buffer = [];
  }
});

console.log("🧠 Omega Quantum Brain ACTIVE");
