const { publish } = require("./event_bus");

const NODE_ID = process.argv[2] || "node-unknown";

setInterval(() => {
    const heartbeat = {
        node: NODE_ID,
        type: "heartbeat",
        cpu: Math.random().toFixed(2),
        memory: Math.random().toFixed(2),
        timestamp: Date.now()
    };

    publish("omega.heartbeat", heartbeat);

    console.log("💓 HEARTBEAT:", heartbeat);
}, 3000);
