console.log("🧠 Cognitive Graph Online");

class Node {
  constructor(id, data = {}) {
    this.id = id;
    this.data = data;
    this.links = [];
    this.energy = Math.random();
  }
}

class Graph {
  constructor() {
    this.nodes = {};
  }

  addNode(id, data) {
    this.nodes[id] = new Node(id, data);
  }

  link(a, b) {
    if (this.nodes[a] && this.nodes[b]) {
      this.nodes[a].links.push(b);
    }
  }

  tick() {
    Object.values(this.nodes).forEach(n => {
      n.energy += (Math.random() - 0.5) * 0.1;
      n.energy = Math.max(0, Math.min(1, n.energy));
    });
  }

  snapshot() {
    return this.nodes;
  }
}

module.exports = Graph;
