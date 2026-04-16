const RedisBus = require("./core/redis_bus");
const VectorMemory = require("./core/vector_memory");
const Reinforcement = require("./core/reinforcement");
const Consensus = require("./core/consensus");
const Worker = require("./workers/worker");

async function start() {
  const bus = new RedisBus();
  await bus.connect();

  const memory = new VectorMemory();
  const rl = new Reinforcement();
  const consensus = new Consensus();

  const worker = new Worker(bus);
  worker.run();

  const votes = [];

  await bus.subscribe("omega_stream", (msg) => {
    memory.store(msg);
    votes.push(msg);

    if (votes.length > 5) {
      const decision = consensus.decide(votes);

      console.log("🧠 CONSENSUS:", decision);

      rl.reward(decision.decision, decision.confidence);

      votes.length = 0;
    }
  });

  console.log("⚡ Omega v8 CORE ONLINE");
}

start();
