const fs = require("fs");

const REG_PATH = process.env.OMEGA_REG || "./omega_registry.json";

function load() {
    try {
        return JSON.parse(fs.readFileSync(REG_PATH));
    } catch {
        return { nodes: {}, brains: {}, lastUpdate: Date.now() };
    }
}

function save(state) {
    state.lastUpdate = Date.now();
    fs.writeFileSync(REG_PATH, JSON.stringify(state, null, 2));
}

function registerNode(id, data) {
    const state = load();
    state.nodes[id] = {
        ...data,
        lastSeen: Date.now()
    };
    save(state);
}

function registerBrain(id, data) {
    const state = load();
    state.brains[id] = {
        ...data,
        lastSeen: Date.now()
    };
    save(state);
}

module.exports = { load, save, registerNode, registerBrain };
