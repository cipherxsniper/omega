import os
from omega_module_classifier_v3 import OmegaModuleClassifierV3

class OmegaManifestBuilderV3:
    def __init__(self):
        self.classifier = OmegaModuleClassifierV3()

    def build(self, path):
        manifest = {
            "kernel": [],
            "service": [],
            "library": [],
            "tool": [],
            "data": []
        }

        for f in os.listdir(path):
            if not f.endswith(".py") and not f.endswith(".json"):
                continue

            category = self.classifier.classify(f)
            manifest[category].append(f)

        return manifest
