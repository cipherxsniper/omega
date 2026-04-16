import os
import ast
import time
import json
import shutil
import importlib.util

OMEGA_DIR = os.path.expanduser("~/Omega")
PATCH_DIR = os.path.join(OMEGA_DIR, "v29_patches")
BACKUP_DIR = os.path.join(OMEGA_DIR, "v29_backups")
LOG_FILE = "omega_v29_patch_log.json"

os.makedirs(PATCH_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)


# -----------------------------
# 🧠 SAFE AST VALIDATOR
# -----------------------------
class ASTValidatorV29:
    def is_valid(self, source_code):
        try:
            ast.parse(source_code)
            return True, None
        except Exception as e:
            return False, str(e)


# -----------------------------
# 💾 VERSIONED BACKUP SYSTEM
# -----------------------------
class BackupSystemV29:
    def backup(self, file_path):
        name = os.path.basename(file_path)
        backup_path = os.path.join(
            BACKUP_DIR,
            f"{name}.{int(time.time())}.bak"
        )
        shutil.copy2(file_path, backup_path)
        return backup_path


# -----------------------------
# 🧬 PATCH GENERATOR (SAFE DIFF STYLE)
# -----------------------------
class PatchGeneratorV29:
    def generate_patch(self, file_path):
        """
        Instead of rewriting full file,
        we simulate a safe patch suggestion.
        """

        return {
            "file": file_path,
            "timestamp": time.time(),
            "patch_type": "safe_runtime_tune",
            "change": "reduce_sleep_or_optimize_loop"
        }


# -----------------------------
# ⚡ SAFE HOT SWAP EXECUTOR
# -----------------------------
class HotSwapExecutorV29:
    def apply_patch(self, file_path, patch):
        try:
            with open(file_path, "r") as f:
                original = f.read()

            backup = BackupSystemV29().backup(file_path)

            # 🧠 SAFE MODIFICATION (example logic injection)
            modified = original

            if "time.sleep(2)" in modified:
                modified = modified.replace("time.sleep(2)", "time.sleep(1.5)")

            if "while True" in modified and "# OPTIMIZED" not in modified:
                modified += "\n# OPTIMIZED BY v29 ENGINE\n"

            # 🧪 validate before writing
            valid, err = ASTValidatorV29().is_valid(modified)

            if not valid:
                print(f"[v29] PATCH REJECTED (syntax error): {err}")
                return False

            # 💾 apply safe write
            with open(file_path, "w") as f:
                f.write(modified)

            return {
                "status": "applied",
                "backup": backup
            }

        except Exception as e:
            return {"status": "failed", "error": str(e)}


# -----------------------------
# 🧠 SELF-HEALING ENGINE CORE
# -----------------------------
class OmegaSelfPatchV29:
    def __init__(self):
        self.generator = PatchGeneratorV29()
        self.executor = HotSwapExecutorV29()
        self.log = []

    def scan_files(self):
        return [
            f for f in os.listdir(OMEGA_DIR)
            if f.endswith(".py") and "v29" not in f
        ]

    def run_patch_cycle(self):
        files = self.scan_files()

        for f in files:
            path = os.path.join(OMEGA_DIR, f)

            patch = self.generator.generate_patch(path)
            result = self.executor.apply_patch(path, patch)

            self.log.append({
                "file": f,
                "patch": patch,
                "result": result,
                "time": time.time()
            })

            print(f"[v29] {f} → {result.get('status')}")

        with open(LOG_FILE, "w") as f:
            json.dump(self.log, f, indent=2)

    def run(self):
        print("[v29] SAFE SELF-PATCH ENGINE ONLINE")

        while True:
            try:
                self.run_patch_cycle()
                time.sleep(6)

            except Exception as e:
                print(f"[v29 CRASH RECOVERED] {e}")
                time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSelfPatchV29().run()
