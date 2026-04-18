class SelfModifier:

    def __init__(self):
        self.patches = []

    def propose_patch(self, node, change):

        self.patches.append({
            "node": node,
            "change": change,
            "status": "pending_review"
        })

    def list_patches(self):
        return self.patches
