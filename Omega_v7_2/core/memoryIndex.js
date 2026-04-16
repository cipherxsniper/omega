class MemoryIndex {
  constructor() {
    this.memory = [];
    this.tagIndex = new Map();
  }

  add(entry) {
    this.memory.push(entry);

    for (const tag of entry.tags || []) {
      if (!this.tagIndex.has(tag)) {
        this.tagIndex.set(tag, []);
      }
      this.tagIndex.get(tag).push(entry.id);
    }
  }

  queryByTag(tag) {
    const ids = this.tagIndex.get(tag) || [];
    return this.memory.filter(m => ids.includes(m.id));
  }

  queryByOutcome(outcome) {
    return this.memory.filter(m => m.outcome === outcome);
  }

  getRecent(limit = 10) {
    return this.memory.slice(-limit);
  }
}

module.exports = MemoryIndex;
