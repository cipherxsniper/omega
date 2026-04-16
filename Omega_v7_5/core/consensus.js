class ConsensusEngine {
  decide(nodes) {
    let score = 0;

    for (const n of nodes) {
      score += n.confidence || 0;
    }

    const avg = score / (nodes.length || 1);

    return {
      decision: avg > 0.5 ? "execute" : "hold",
      confidence: avg
    };
  }
}

module.exports = ConsensusEngine;
