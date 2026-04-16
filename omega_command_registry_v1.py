import os
import importlib.util
import traceback

# =========================
# 🧠 OMEGA COMMAND REGISTRY v1
# =========================

COMMANDS = {}

COMMAND_DIR = "commands"


# =========================
# 🔌 LOAD PLUGIN COMMAND
# =========================

def load_plugin(path):
    try:
        name = os.path.basename(path).replace(".py", "")

        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "register"):
            module.register(COMMANDS)

        print(f"[Ω-REGISTRY] Loaded: {name}")

    except Exception:
        print(f"[Ω-REGISTRY ERROR] Failed loading {path}")
        traceback.print_exc()


# =========================
# ⚡ SCAN COMMAND DIRECTORY
# =========================

def scan_commands():
    if not os.path.exists(COMMAND_DIR):
        return

    for file in os.listdir(COMMAND_DIR):
        if file.endswith(".py"):
            load_plugin(os.path.join(COMMAND_DIR, file))


# =========================
# 🧠 REGISTER COMMAND
# =========================

def register(name, func):
    COMMANDS[name] = func


# =========================
# 🚀 EXECUTE COMMAND
# =========================

def execute(cmd, args):
    if cmd in COMMANDS:
        try:
            COMMANDS[cmd](args)
        except Exception:
            print(f"[Ω-ERROR] command failed: {cmd}")
            traceback.print_exc()
    else:
        print(f"[Ω] Unknown command: {cmd}")


# =========================
# 🌐 CORE BUILT-IN COMMANDS
# =========================

def install_core_commands():

    def ls(args):
        print("\n".join(os.listdir(".")))

    def run_all(args):
        print("[Ω] Running all Python files...")
        for f in os.listdir("."):
            if f.endswith(".py"):
                os.system(f"nohup python {f} > logs/{f}.log 2>&1 &")

    def run_swarm(args):
        print("[Ω] Launching swarm mode...")
        os.system("bash run_omega_mesh_v13_v17.sh")

    def ps(args):
        os.system("ps -aux | head -n 20")

    COMMANDS["ls"] = ls
    COMMANDS["run_all"] = run_all
    COMMANDS["run_swarm"] = run_swarm
    COMMANDS["ps"] = ps


# =========================
# 🚀 BOOTSTRAP REGISTRY
# =========================

def boot_registry():
    print("[Ω] Booting command registry v1...")
    install_core_commands()
    scan_commands()
    print(f"[Ω] Commands loaded: {list(COMMANDS.keys())}")


if __name__ == "__main__":
    boot_registry()

    while True:
        try:
            raw = input("~omega$ ").strip()
            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0]
            args = parts[1:]

            execute(cmd, args)

        except KeyboardInterrupt:
            print("\n[Ω] shutdown")
            break
