class MetaLearningLayer {
  constructor() {
    this.strategyWeights = {
      scalp: 1.0,
      trend_follow: 1.0,
      mean_reversion: 1.0
    };
  }

  learn(entry) {
    const reward = entry.outcome === "profit" ? 1 : -1;

    for (const tag of entry.tags || []) {
      if (this.strategyWeights[tag] !== undefined) {
        this.strategyWeights[tag] += reward * 0.05;

        this.strategyWeights[tag] = Math.max(
          0.1,
          Math.min(2.0, this.strategyWeights[tag])
        );
      }
    }
  }

  recommend(tags = []) {
    let score = 0;

    for (const t of tags) {
      score += this.strategyWeights[t] || 0;
    }

    return score / (tags.length || 1);
  }

  getWeights() {
    return this.strategyWeights;
  }
}

module.exports = MetaLearningLayer;
