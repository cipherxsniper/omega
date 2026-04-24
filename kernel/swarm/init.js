const Graph = require("./graph");

console.log("⚡ Initializing Omega Swarm...");

const g = new Graph();

g.addNode("brain");
g.addNode("memory");
g.addNode("orchestrator");
g.addNode("workers");

g.link("brain", "memory");
g.link("brain", "orchestrator");
g.link("orchestrator", "workers");

module.exports = g;
