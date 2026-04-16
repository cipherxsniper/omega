# ============================================================
# OMEGA LEARNING ENGINE PATCH v1
# Fixes missing learn() crash
# ============================================================

import random

class OmegaLearningEngine:

    def __init__(self, memory=None):
        self.memory = memory
        self.patterns = []
        self.last_output = None

    def learn(self, data=None):
        """Main learning entry point (FIXED)"""
        if self.memory:
            data = self.memory.retrieve()

        if not data:
            return []

        # simple pattern extraction (safe default)
        patterns = []
        for item in data:
            if isinstance(item, dict):
                patterns.extend(item.keys())

        self.patterns = list(set(patterns))
        self.last_output = self.patterns

        return self.patterns

    def reinforce(self):
        """strengthen patterns"""
        return {"reinforced": len(self.patterns)}

    def get_patterns(self):
        return self.patterns
