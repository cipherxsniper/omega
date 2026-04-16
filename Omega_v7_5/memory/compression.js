class MemoryCompression {
  constructor() {
    this.store = [];
  }

  add(entry) {
    this.store.push(entry);
  }

  compress() {
    const map = new Map();

    for (const m of this.store) {
      const key = (m.type || "unknown") + ":" + (m.outcome || "none");

      if (!map.has(key)) {
        map.set(key, { count: 0, score: 0 });
      }

      const obj = map.get(key);
      obj.count += 1;
      obj.score += m.score || 0;
    }

    const compressed = [];

    for (const [key, val] of map.entries()) {
      compressed.push({
        key,
        avgScore: val.score / val.count,
        volume: val.count
      });
    }

    return compressed;
  }
}

module.exports = MemoryCompression;
