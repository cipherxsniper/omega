class SelfModifyEngine:

    def __init__(self, governance):
        self.governance = governance

    def propose_patch(self, patch_id, file, change):
        proposal = {
            "file": file,
            "change": change
        }

        self.governance.propose_change(patch_id, proposal)
        return f"Patch proposed: {patch_id}"

    def apply_patch(self, patch_id):
        if self.governance.resolve(patch_id):
            return f"Patch {patch_id} APPROVED and applied"
        else:
            return f"Patch {patch_id} REJECTED"
