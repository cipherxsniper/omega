console.log("🧠 Omega Orchestrator Online");

// Simple subsystem loader (safe mode)
const subsystems = [
  "brain",
  "memory",
  "node",
  "workers"
];

subsystems.forEach(s => {
  console.log("🔌 Loading subsystem:", s);
});

console.log("✅ Omega system stable (safe mode)");
