import os
import time
import json
import socket
import threading

# -----------------------------
# CONFIG
# -----------------------------
KERNEL_NAME = "OMEGA KERNEL V4"
PORT = 5050
LOCK_FILE = os.path.expanduser("~/.omega_kernel_v4.lock")
LOG_FILE = "omega_v4.log"


# -----------------------------
# SINGLE INSTANCE LOCK
# -----------------------------
def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = f.read().strip()
            print(f"[KERNEL V4] Already running (PID {pid}) → EXIT")
        except:
            print("[KERNEL V4] Already running → EXIT")
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
# SAFE STATE ENGINE
# -----------------------------
class KernelState:
    def __init__(self):
        self.step = 0
        self.memory = []
        self.last_heartbeat = time.time()

    def tick(self):
        self.step += 1
        self.last_heartbeat = time.time()
        return self.step


# -----------------------------
# SWARM NETWORK (SAFE)
# -----------------------------
class SwarmNetwork:
    def __init__(self, port=5050):
        self.port = int(port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def listen(self, state):
        try:
            self.sock.bind(("127.0.0.1", int(self.port)))
            print(f"[SWARM] listening on {self.port}")
        except Exception as e:
            print(f"[SWARM ERROR] bind failed: {e}")
            return

        while True:
            try:
                data, _ = self.sock.recvfrom(4096)
                msg = json.loads(data.decode(errors="ignore"))
                state.memory.append(msg)
                print("[SWARM IN]", msg)
            except Exception as e:
                print(f"[SWARM ERROR] recv failed: {e}")

    def broadcast(self, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)

            self.sock.sendto(
                message.encode(),
                ("127.0.0.1", self.port)
            )
        except Exception as e:
            print(f"[SWARM ERROR] broadcast failed: {e}")


# -----------------------------
# KERNEL CORE
# -----------------------------
class OmegaKernelV4:
    def __init__(self):
        self.state = KernelState()
        self.swarm = SwarmNetwork(PORT)
        self.running = True

    def boot(self):
        print(f"[KERNEL V4] {KERNEL_NAME} ONLINE")

        threading.Thread(
            target=self.swarm.listen,
            args=(self.state,),
            daemon=True
        ).start()

        while self.running:
            try:
                step = self.state.tick()

                msg = {
                    "type": "heartbeat",
                    "step": step,
                    "time": time.time()
                }

                self.swarm.broadcast(msg)

                print(f"[KERNEL] tick {step}")

                time.sleep(2)

            except Exception as e:
                print(f"[KERNEL ERROR] {e}")
                time.sleep(1)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    if not acquire_lock():
        exit()

    try:
        OmegaKernelV4().boot()
    except KeyboardInterrupt:
        print("\n[KERNEL V4] shutting down...")
    finally:
        release_lock()
