# OMEGA SAFE IMPORT ENGINE v1
# Controlled module resolution (NO global import hijacking)

import os
import sys
import re
from pathlib import Path

OMEGA_ROOT = Path(__file__).resolve().parents[1]


class SafeImportResolver:
    def __init__(self):
        self.index = self.scan()

    def scan(self):
        index = {}
        for root, _, files in os.walk(OMEGA_ROOT):
            for f in files:
                if f.endswith(".py"):
                    name = f[:-3]
                    index[name] = Path(root) / f
        return index

    def resolve(self, module_name: str):
        if module_name in self.index:
            return self.index[module_name]

        base = re.sub(r"_v\d+.*$", "", module_name)

        for k, v in self.index.items():
            if k.startswith(base):
                return v

        return None


RESOLVER = SafeImportResolver()


def safe_import(module_name: str):
    """
    Safe lookup only. Does NOT execute sys.meta_path tricks.
    """
    return RESOLVER.resolve(module_name)
