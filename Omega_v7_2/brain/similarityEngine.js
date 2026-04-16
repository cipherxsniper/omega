class SimilarityEngine {
  similarity(a, b) {
    let score = 0;

    const aTags = new Set(a.tags || []);
    const bTags = new Set(b.tags || []);

    const intersection = [...aTags].filter(t => bTags.has(t)).length;
    const union = new Set([...aTags, ...bTags]).size;

    if (union > 0) {
      score += intersection / union;
    }

    if (a.outcome && b.outcome && a.outcome === b.outcome) {
      score += 0.3;
    }

    const ca = a.context?.confidence;
    const cb = b.context?.confidence;

    if (ca && cb) {
      score += (1 - Math.abs(ca - cb)) * 0.2;
    }

    return score;
  }

  findSimilar(target, memory, threshold = 0.5) {
    return memory
      .map(m => ({ m, score: this.similarity(target, m) }))
      .filter(x => x.score >= threshold)
      .sort((a, b) => b.score - a.score);
  }
}

module.exports = SimilarityEngine;
