const Redis = require("redis");
const EventStore = require("./event_store");

const store = new EventStore();

(async () => {
  const sub = Redis.createClient();
  await sub.connect();

  await sub.subscribe("omega_stream", (msg) => {
    const data = JSON.parse(msg);

    store.append(data);

    console.log("📡 SWARM:", data.node, data.confidence);
  });

  console.log("🧠 Omega v10 Core ONLINE");
})();
