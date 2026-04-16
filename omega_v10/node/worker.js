const Redis = require("redis");

(async () => {
  const client = Redis.createClient();
  await client.connect();

  setInterval(async () => {
    const msg = {
      node: "js_worker",
      confidence: Math.random(),
      action: Math.random() > 0.5 ? "explore" : "exploit"
    };

    await client.publish("omega_stream", JSON.stringify(msg));
  }, 300);

  console.log("⚙️ JS Worker ONLINE");
})();
