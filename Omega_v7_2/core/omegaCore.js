const MemoryIndex = require("./memoryIndex");
const SimilarityEngine = require("../brain/similarityEngine");
const MetaLearningLayer = require("../brain/metaLearning");

class OmegaCore {
  constructor() {
    this.memory = new MemoryIndex();
    this.similarity = new SimilarityEngine();
    this.meta = new MetaLearningLayer();
  }

  ingest(entry) {
    this.memory.add(entry);
    this.meta.learn(entry);
  }

  recallSimilar(entry) {
    return this.similarity.findSimilar(entry, this.memory.memory);
  }

  strategyScore(tags) {
    return this.meta.recommend(tags);
  }

  snapshot() {
    return {
      memorySize: this.memory.memory.length,
      weights: this.meta.getWeights(),
      recent: this.memory.getRecent(5)
    };
  }
}

module.exports = OmegaCore;
