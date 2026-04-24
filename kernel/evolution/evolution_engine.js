console.log("🧬 Omega Evolution Engine Online");

const fs = require("fs");

let evolutionState = {
  cycle: 0,
  stability: 1.0,
  mutations: 0
};

function evolve() {
  evolutionState.cycle++;

  // simulate system adaptation
  if (Math.random() > 0.7) {
    evolutionState.stability -= 0.01;
    evolutionState.mutations++;
  } else {
    evolutionState.stability += 0.005;
  }

  evolutionState.stability = Math.max(0, Math.min(1, evolutionState.stability));

  console.log("🧬 Cycle:", evolutionState.cycle);
  console.log("📊 Stability:", evolutionState.stability.toFixed(3));
  console.log("🧪 Mutations:", evolutionState.mutations);

  fs.writeFileSync(
    "./runtime_state/evolution.json",
    JSON.stringify(evolutionState, null, 2)
  );
}

module.exports = { evolve, evolutionState };
