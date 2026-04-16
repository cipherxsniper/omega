
const fs = require("fs");

const NODE_ID = "node_js_" + process.pid;

setInterval(() => {
  let registry = JSON.parse(fs.readFileSync("../core/node_registry.json"));

  registry.nodes[NODE_ID] = {
    type: "js",
    last_seen: Date.now(),
    load: Math.random()
  };

  fs.writeFileSync("../core/node_registry.json", JSON.stringify(registry, null, 2));
}, 2000);
