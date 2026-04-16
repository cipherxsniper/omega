import os
import time
import json
import socket
import threading
import sys

# -----------------------------
# CONFIG
# -----------------------------
KERNEL_NAME = "OMEGA KERNEL V5"
PORT = 5050
LOCK_FILE = os.path.expanduser("~/.omega_kernel_v5.lock")

# -----------------------------
# SAFE LOCK SYSTEM
# -----------------------------
def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = f.read().strip()
            print(f"[KERNEL V5] Already running (PID {pid}) → exiting")
        except:
            print("[KERNEL V5] Already running → exiting")
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
# SWARM NETWORK (SAFE)
# -----------------------------
class SwarmNetwork:
    def __init__(self, port=5050):
        self.port = int(port)
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def listen(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # SAFE REBIND (avoid crash)
            try:
                s.bind(("127.0.0.1", int(self.port)))
            except OSError:
                print(f"[SWARM] Port {self.port} busy → skipping bind")
                return

            print(f"[SWARM] listening on {self.port}")

            while self.running:
                try:
                    data, addr = s.recvfrom(4096)
                    msg = data.decode(errors="ignore")
                    print("[SWARM IN]", msg)
                except Exception as e:
                    print("[SWARM ERROR]", str(e))

        except Exception as e:
            print("[SWARM FATAL]", str(e))

    def broadcast(self, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)

            if not isinstance(message, (str, bytes)):
                message = str(message)

            self.sock.sendto(
                message.encode(),
                ("127.0.0.1", int(self.port))
            )
        except Exception as e:
            print("[SWARM ERROR]", "broadcast failed:", e)


# -----------------------------
# CONTROLLED KERNEL LOOP
# -----------------------------
class OmegaKernelV5:
    def __init__(self):
        self.swarm = SwarmNetwork(PORT)
        self.tick = 0
        self.running = True

    def boot(self):
        print(f"[{KERNEL_NAME}] ONLINE")

        t = threading.Thread(target=self.swarm.listen, daemon=True)
        t.start()

        try:
            while self.running:
                self.tick += 1

                print(f"[KERNEL] tick {self.tick}")

                self.swarm.broadcast({
                    "type": "heartbeat",
                    "step": self.tick,
                    "time": time.time()
                })

                time.sleep(2)

        except KeyboardInterrupt:
            print("\n[KERNEL V5] Shutting down...")
            self.running = False
            self.swarm.running = False
            release_lock()
            sys.exit(0)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    if not acquire_lock():
        sys.exit(0)

    OmegaKernelV5().boot()
