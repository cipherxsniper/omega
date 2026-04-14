import os
import time
import json
import socket
import threading

# -----------------------------
# CONFIG (SAFE DEFAULTS)
# -----------------------------
HOST = "127.0.0.1"
PORT = 5050

LOCK_FILE = os.path.expanduser("~/Omega/.omega_kernel.lock")


# -----------------------------
# SAFE SINGLE INSTANCE LOCK
# -----------------------------
def acquire_lock():
    os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)

    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                old = f.read().strip()
            print(f"[KERNEL V3] Already running (PID {old})")
        except:
            print("[KERNEL V3] Already running")
        return False

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True


def release_lock():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass


# -----------------------------
# 🧠 SAFE SWARM NETWORK (FIXED)
# -----------------------------
class SwarmNetwork:
    def __init__(self, port=5050):
        self.port = int(port)
        self.sock = None
        self.running = True

    def _create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s

    # -------------------------
    # LISTEN (CRASH SAFE)
    # -------------------------
    def listen(self):
        try:
            self.sock = self._create_socket()
            try:
                self.sock.bind((HOST, self.port))
            except OSError:
                print(f"[SWARM] Port {self.port} busy → continuing without bind")
                return

            print(f"[SWARM] listening on {self.port}")

            while self.running:
                try:
                    data, _ = self.sock.recvfrom(4096)
                    msg = data.decode(errors="ignore")
                    print("[SWARM IN]", msg)
                except Exception as e:
                    print("[SWARM ERROR]", e)

        except Exception as e:
            print("[SWARM FATAL]", e)

    # -------------------------
    # BROADCAST (TYPE SAFE FIX)
    # -------------------------
    def broadcast(self, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)

            if not isinstance(message, (str, bytes)):
                message = str(message)

            s = self._create_socket()
            s.sendto(message.encode(), (HOST, self.port))
            s.close()

        except Exception as e:
            print("[SWARM BROADCAST ERROR]", e)


# -----------------------------
# 🧠 MINIMAL SAFE KERNEL CORE
# -----------------------------
class OmegaKernelV3:
    def __init__(self):
        self.swarm = SwarmNetwork(PORT)

    def boot(self):
        print("[KERNEL V3] OMEGA ZERO-CRASH KERNEL ONLINE")

        t = threading.Thread(target=self.swarm.listen, daemon=True)
        t.start()

        step = 0

        while True:
            step += 1

            heartbeat = {
                "type": "heartbeat",
                "status": "alive",
                "step": step,
                "time": time.time()
            }

            self.swarm.broadcast(heartbeat)

            print(f"[KERNEL] tick {step}")

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    if not acquire_lock():
        exit(0)

    try:
        OmegaKernelV3().boot()
    except KeyboardInterrupt:
        print("\n[KERNEL V3] Shutdown")
    finally:
        release_lock()
