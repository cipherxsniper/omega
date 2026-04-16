const Redis = require("redis");

(async () => {
  const sub = Redis.createClient();
  await sub.connect();

  let count = 0;
  let avg = 0;

  await sub.subscribe("omega_stream", (msg) => {
    const data = JSON.parse(msg);

    avg = (avg * count + (data.confidence || 0)) / (count + 1);
    count++;

    console.log("📊 Swarm:", avg.toFixed(3));
  });

  console.log("🧠 Omega v10 Core ONLINE");
})();
