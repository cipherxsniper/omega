import re
import sys
from pathlib import Path

# ================================
# OMEGA IMPORT REPAIR MAP
# ================================
IMPORT_MAP = {
    "core.": "omega_layers.v10.core.",
}

# ================================
# READ FILE
# ================================
def load_file(path):
    return Path(path).read_text()

def save_file(path, content):
    Path(path).write_text(content)

# ================================
# REWRITE IMPORTS
# ================================
def repair_imports(code):
    lines = code.splitlines()
    new_lines = []

    changed = False

    for line in lines:
        fixed = line

        # only target import lines
        if "import" in line or "from" in line:

            for old, new in IMPORT_MAP.items():
                if old in line:
                    fixed = fixed.replace(old, new)
                    changed = True

        new_lines.append(fixed)

    return "\n".join(new_lines), changed

# ================================
# VALIDATION
# ================================
def validate_syntax(code):
    try:
        compile(code, "<omega_patch>", "exec")
        return True
    except Exception as e:
        print("❌ SYNTAX ERROR AFTER PATCH:")
        print(e)
        return False

# ================================
# MAIN REPAIR ENGINE
# ================================
def run_repair(file_path):
    file_path = Path(file_path)

    print("\n🧠 OMEGA AUTO IMPORT REPAIR v10\n")

    original = load_file(file_path)
    patched, changed = repair_imports(original)

    if not changed:
        print("🟡 No import issues detected")
        return

    print("\n🛠 PATCH APPLIED\n")

    print("──────── BEFORE ────────")
    print(original[:500])

    print("\n──────── AFTER ────────")
    print(patched[:500])

    if validate_syntax(patched):
        save_file(file_path, patched)
        print("\n🟢 FILE UPDATED SAFELY")
    else:
        print("\n🔴 PATCH ABORTED (syntax invalid)")

# ================================
# ENTRY
# ================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python omega_auto_import_repair_v10.py <file>")
    else:
        run_repair(sys.argv[1])
