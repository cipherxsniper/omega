# ============================================================
# OMEGA MEMORY PATCH v1 (COMPATIBILITY LAYER)
# Fixes missing .store() / .retrieve() across system
# ============================================================

class OmegaGlobalMemoryCloud:

    def __init__(self):
        self.data = []
        self.index = {}

    # =========================
    # REQUIRED STANDARD API
    # =========================

    def store(self, payload):
        """Universal memory write"""
        self.data.append(payload)

        # lightweight indexing
        if isinstance(payload, dict):
            for k, v in payload.items():
                self.index[k] = v

    def retrieve(self, key=None):
        """Universal memory read"""
        if key is None:
            return self.data[-50:]  # recent memory

        return self.index.get(key, None)

    def query(self):
        """Return full memory snapshot"""
        return {
            "size": len(self.data),
            "index_keys": list(self.index.keys())
        }
