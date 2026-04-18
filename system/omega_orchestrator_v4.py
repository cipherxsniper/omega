from core.omega_swarm import OmegaSwarm
from core.omega_attention import OmegaAttention
from core.omega_consensus import OmegaConsensus
from core.omega_predictor import OmegaPredictor
from core.omega_memory_compressor import OmegaMemoryCompressor

class OmegaOrchestratorV4:

    def __init__(self):
        self.swarm = OmegaSwarm(size=5)

        self.attn = OmegaAttention()
        self.consensus = OmegaConsensus()
        self.predictor = OmegaPredictor()
        self.compressor = OmegaMemoryCompressor()

        self.tick = 0

    def run_cycle(self):

        raw_events = [{"x": 1, "y": 0.3}, {"x": -0.4, "y": 0.6}, {"x": 0.1, "y": 0.05}]

        # 1. Attention filter
        events = self.attn.filter(raw_events)

        # 2. Swarm processing
        outputs = self.swarm.step(events)

        # 3. Consensus formation
        consensus = self.consensus.merge(outputs)

        # 4. Compression stabilization
        stable = self.compressor.compress(consensus)

        # 5. Prediction
        future = self.predictor.predict(stable)

        if self.tick % 5 == 0:
            print("🧠 CONSENSUS:", stable)
            print("🔮 PREDICTION:", future)

        self.tick += 1
