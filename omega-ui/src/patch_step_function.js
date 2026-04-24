// 🌱 ECOSYSTEM + UNIVERSE MAIN LOOP PATCH
// INSERT INSIDE step() FUNCTION IN App.js

// 🌱 ecosystem update
ecosystems = updateEcosystems(ecosystems);

// 🌌 universe evolution
universes = updateUniverses(ecosystems, universes);

// 🧠 assign particles → ecosystems
particles.forEach(p => {
  p.eco = assignEcosystem(p, ecosystems);
});
