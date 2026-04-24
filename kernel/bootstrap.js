const fs = require("fs");
const path = require("path");

function loadModules() {
  console.log("📦 Loading Omega Registry...");

  const registryPath = path.join(__dirname, "../registry/modules.json");

  if (!fs.existsSync(registryPath)) {
    console.log("⚠️ No registry found, creating default...");
    fs.writeFileSync(registryPath, JSON.stringify({
      modules: ["core", "brain", "memory"]
    }, null, 2));
  }

  const registry = JSON.parse(fs.readFileSync(registryPath));

  console.log("🔌 Registered Modules:", registry.modules);

  registry.modules.forEach(m => {
    console.log("⚡ Activating module:", m);
  });

  console.log("✅ Omega Runtime Ready");
}

module.exports = loadModules;
