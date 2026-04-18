import time
import uuid
import copy
from datetime import datetime

from omega.core.global_memory import GLOBAL_MEMORY
from omega.core.self_rewriting_engine import SelfRewritingEngine

ENGINE = SelfRewritingEngine()

class EvolutionKernelV8:
    """
    Controlled self-evolving system:
    - nodes propose mutations
    - kernel scores them
    - only approved mutations are applied
    """

    def __init__(self):
        self.mutation_pool = []
        self.applied_mutations = []
        self.rejection_pool = []

    # ---------------------------
    # 1. PROPOSAL PHASE
    # ---------------------------
    def propose_mutation(self, node_name, mutation_type, payload):
        mutation = {
            "id": str(uuid.uuid4()),
            "node": node_name,
            "type": mutation_type,
            "payload": payload,
            "time": datetime.utcnow().isoformat(),
            "status": "pending"
        }

        self.mutation_pool.append(mutation)
        GLOBAL_MEMORY["mutations"] = self.mutation_pool

        return mutation

    # ---------------------------
    # 2. SCORING PHASE
    # ---------------------------
    def score_mutation(self, mutation):
        score = 0.5  # baseline

        # reward contract compliance fixes
        if mutation["type"] == "contract_patch":
            score += 0.25

        # reward stability improvements
        if "stability" in str(mutation["payload"]):
            score += 0.2

        # penalize unknown mutations
        if mutation["type"] not in [
            "contract_patch",
            "dependency_patch",
            "interface_patch"
        ]:
            score -= 0.3

        return max(0.0, min(1.0, score))

    # ---------------------------
    # 3. SELECTION PHASE
    # ---------------------------
    def select_mutations(self):
        approved = []

        for m in self.mutation_pool:
            score = self.score_mutation(m)

            if score >= 0.65:
                m["score"] = score
                m["status"] = "approved"
                approved.append(m)
            else:
                m["score"] = score
                m["status"] = "rejected"
                self.rejection_pool.append(m)

        return approved

    # ---------------------------
    # 4. APPLICATION PHASE
    # ---------------------------
    def apply_mutation(self, mutation):
        try:
            node_file = mutation["payload"].get("file")
            patch = mutation["payload"].get("patch")

            if not node_file or not patch:
                return False

            with open(node_file, "a") as f:
                f.write("\n\n# === V8 EVOLUTION PATCH ===\n")
                f.write(str(patch))

            self.applied_mutations.append(mutation)
            return True

        except Exception as e:
            ENGINE.capture_failure("kernel", e)
            return False

    # ---------------------------
    # 5. EVOLUTION LOOP
    # ---------------------------
    def run_cycle(self):
        approved = self.select_mutations()

        for m in approved:
            self.apply_mutation(m)

        # cleanup
        self.mutation_pool = []

        return {
            "approved": len(approved),
            "rejected": len(self.rejection_pool)
        }
