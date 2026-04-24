console.log("🔁 Hot Module System Online");

const loadedModules = {};

function loadModule(name, path) {
  delete require.cache[require.resolve(path)];
  loadedModules[name] = require(path);
  console.log("⚡ Loaded module:", name);
}

function reloadModule(name, path) {
  console.log("🔄 Reloading:", name);
  loadModule(name, path);
}

function getModule(name) {
  return loadedModules[name];
}

module.exports = {
  loadModule,
  reloadModule,
  getModule
};
