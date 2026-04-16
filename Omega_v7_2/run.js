const OmegaCore = require("./core/omegaCore");

const omega = new OmegaCore();

// sample data
omega.ingest({
  id: "1",
  type: "trade",
  context: { confidence: 0.8 },
  outcome: "profit",
  tags: ["scalp", "trend_follow"]
});

omega.ingest({
  id: "2",
  type: "trade",
  context: { confidence: 0.6 },
  outcome: "loss",
  tags: ["mean_reversion"]
});

omega.ingest({
  id: "3",
  type: "trade",
  context: { confidence: 0.9 },
  outcome: "profit",
  tags: ["scalp"]
});

// test similarity
const query = {
  id: "query",
  context: { confidence: 0.85 },
  outcome: "profit",
  tags: ["scalp"]
};

console.log("🔍 Similar:", omega.recallSimilar(query));
console.log("📊 Strategy Score:", omega.strategyScore(["scalp"]));
console.log("🧠 Snapshot:", omega.snapshot());
