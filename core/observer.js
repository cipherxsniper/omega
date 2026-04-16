const { subscribe } = require("./event_bus");

let nodes = new Set();

function describe(h) {
    return `
🧠 OMEGA OBSERVER
--------------------------
Node: ${h.node}
Type: ${h.type}
CPU Load: ${(h.cpu * 100).toFixed(1)}%
Memory Load: ${(h.memory * 100).toFixed(1)}%
Status: ACTIVE
Time: ${new Date(h.timestamp).toLocaleTimeString()}
--------------------------
`;
}

subscribe("omega.heartbeat", (data) => {
    nodes.add(data.node);

    console.log(describe(data));

    console.log(`📊 Total Active Nodes: ${nodes.size}`);
});
