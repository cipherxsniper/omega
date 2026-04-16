import re
from pathlib import Path

CANON_ROOT = "omega_layers.v10"

def normalize_import(line: str) -> str:
    line = line.strip()

    if not line.startswith("from "):
        return line

    # extract module path
    match = re.match(r"from\s+([a-zA-Z0-9_\.]+)\s+import", line)
    if not match:
        return line

    module = match.group(1)

    # ❌ prevent double prefixing
    if module.count(CANON_ROOT) > 1:
        parts = module.split(CANON_ROOT)
        module = CANON_ROOT + parts[-1]

    # ❌ fix raw "core." style imports
    if module.startswith("core."):
        module = f"{CANON_ROOT}.core" + module[len("core"):]

    # ❌ fix missing root
    elif not module.startswith(CANON_ROOT):
        module = f"{CANON_ROOT}.{module}"

    return line.replace(match.group(1), module)


def repair_file(path):
    p = Path(path)
    code = p.read_text()

    fixed_lines = []
    for line in code.splitlines():
        if "from " in line:
            fixed_lines.append(normalize_import(line))
        else:
            fixed_lines.append(line)

    new_code = "\n".join(fixed_lines)

    print("\n🧠 IMPORT CANONICALIZER V1")
    print("\n──────── FIX PREVIEW ────────")
    print(new_code[:600])

    p.write_text(new_code)
    print("\n🟢 IMPORTS CANONICALIZED SAFE")


if __name__ == "__main__":
    import sys
    repair_file(sys.argv[1])
