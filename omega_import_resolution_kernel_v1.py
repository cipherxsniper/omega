import re
import sys
from pathlib import Path

# ================================
# OMEGA IMPORT KERNEL v1
# ================================

CANONICAL_PREFIX = "omega_layers.v10."

VALID_DOMAINS = [
    "core",
    "runtime",
    "policies",
    "memory",
    "graph",
    "identity"
]

# ================================
# LOAD / SAVE
# ================================
def load_file(path):
    return Path(path).read_text()

def save_file(path, content):
    Path(path).write_text(content)

# ================================
# DETECT IMPORTS
# ================================
def is_import_line(line):
    return line.strip().startswith("import ") or line.strip().startswith("from ")

# ================================
# NORMALIZATION ENGINE
# ================================
def normalize_import(line):
    original = line

    # Fix double omega_layers injection
    line = re.sub(r"(omega_layers\.v10\.)+", "omega_layers.v10.", line)

    # Remove legacy "core." prefix
    line = line.replace("core.", CANONICAL_PREFIX + "core.")
    line = line.replace("runtime.", CANONICAL_PREFIX + "runtime.")

    # Fix broken duplicates like omega_layers.v10.omega_layers.v10
    while "omega_layers.v10.omega_layers.v10" in line:
        line = line.replace(
            "omega_layers.v10.omega_layers.v10",
            "omega_layers.v10"
        )

    # Ensure canonical prefix exists for internal Omega modules
    if "omega_" in line and CANONICAL_PREFIX not in line:
        parts = line.split()
        for i, p in enumerate(parts):
            if "omega_" in p:
                parts[i] = CANONICAL_PREFIX + p
        line = " ".join(parts)

    return line, (line != original)

# ================================
# MAIN REPAIR ENGINE
# ================================
def repair_file(path):
    print("\n🧠 OMEGA IMPORT RESOLUTION KERNEL v1\n")

    code = load_file(path)
    lines = code.splitlines()

    new_lines = []
    changes = 0

    for line in lines:
        if is_import_line(line):
            fixed, changed = normalize_import(line)
            if changed:
                changes += 1
                print(f"🛠 FIXED: {line.strip()}")

            new_lines.append(fixed)
        else:
            new_lines.append(line)

    new_code = "\n".join(new_lines)

    # Validate
    try:
        compile(new_code, "<omega_import_kernel>", "exec")
    except Exception as e:
        print("\n❌ KERNEL ABORT: syntax invalid after patch")
        print(e)
        return

    save_file(path, new_code)

    print("\n🟢 IMPORT RESOLUTION COMPLETE")
    print(f"📦 Fixes applied: {changes}")

# ================================
# ENTRY
# ================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python omega_import_resolution_kernel_v1.py <file>")
    else:
        repair_file(sys.argv[1])
