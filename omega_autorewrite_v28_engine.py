import os
import ast
import json
import time
import shutil
import random

OMEGA_DIR = os.path.expanduser("~/Omega")

PATCH_LOG = "omega_v28_patch_log.json"
BACKUP_DIR = os.path.join(OMEGA_DIR, "v28_backups")

os.makedirs(BACKUP_DIR, exist_ok=True)


# -----------------------------
# 🧬 CODE ANALYZER (AST ENGINE)
# -----------------------------
class CodeAnalyzerV28:
    def analyze(self, file_path):
        try:
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())

            stats = {
                "functions": 0,
                "loops": 0,
                "imports": 0,
                "classes": 0
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    stats["functions"] += 1
                elif isinstance(node, (ast.For, ast.While)):
                    stats["loops"] += 1
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    stats["imports"] += 1
                elif isinstance(node, ast.ClassDef):
                    stats["classes"] += 1

            return stats

        except Exception as e:
            return {"error": str(e)}


# -----------------------------
# 🧠 PATCH ENGINE (SAFE SUGGESTIONS ONLY)
# -----------------------------
class PatchEngineV28:
    def suggest_patch(self, file_path, analysis):
        suggestions = []

        if analysis.get("loops", 0) > 10:
            suggestions.append("reduce_loop_complexity")

        if analysis.get("imports", 0) > 20:
            suggestions.append("optimize_imports")

        if analysis.get("functions", 0) > 50:
            suggestions.append("modularize_code")

        if not suggestions:
            suggestions.append("no_change_needed")

        return {
            "file": file_path,
            "timestamp": time.time(),
            "analysis": analysis,
            "suggestion": random.choice(suggestions)
        }


# -----------------------------
# 💾 SAFE BACKUP SYSTEM
# -----------------------------
class BackupSystemV28:
    def backup(self, file_path):
        try:
            name = os.path.basename(file_path)
            backup_path = os.path.join(
                BACKUP_DIR,
                f"{name}.{int(time.time())}.bak"
            )
            shutil.copy2(file_path, backup_path)
            return backup_path
        except:
            return None


# -----------------------------
# 🧬 AUTONOMOUS REWRITE CORE
# -----------------------------
class OmegaSelfRewriteV28:
    def __init__(self):
        self.analyzer = CodeAnalyzerV28()
        self.patcher = PatchEngineV28()
        self.backup = BackupSystemV28()

        self.log_data = []

    def scan_files(self):
        return [
            f for f in os.listdir(OMEGA_DIR)
            if f.endswith(".py") and "v28" not in f
        ]

    def evaluate(self, file_path):
        full_path = os.path.join(OMEGA_DIR, file_path)

        analysis = self.analyzer.analyze(full_path)
        patch = self.patcher.suggest_patch(full_path, analysis)

        return patch

    # -----------------------------
    # 🧠 SAFE APPLY LAYER
    # -----------------------------
    def apply_patch(self, patch):
        file_path = patch["file"]

        # backup first
        backup = self.backup.backup(file_path)

        log_entry = {
            "file": file_path,
            "backup": backup,
            "patch": patch,
            "status": "evaluated_only"
        }

        self.log_data.append(log_entry)

        print(f"[v28] evaluated {file_path} → {patch['suggestion']}")

    # -----------------------------
    # 🔁 MAIN LOOP
    # -----------------------------
    def run(self):
        print("[v28] AUTONOMOUS REWRITE ENGINE ONLINE")

        while True:
            files = self.scan_files()

            for f in files:
                full_path = os.path.join(OMEGA_DIR, f)
                patch = self.evaluate(f)
                self.apply_patch(patch)

            # persist log
            with open(PATCH_LOG, "w") as f:
                json.dump(self.log_data, f, indent=2)

            time.sleep(5)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSelfRewriteV28().run()
