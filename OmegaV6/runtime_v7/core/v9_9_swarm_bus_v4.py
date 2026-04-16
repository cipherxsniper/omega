import socket
import json
import time
import threading
import traceback
from collections import deque

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV4:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠⚙️ [SWARM BUS V4] INITIALIZING RELIABLE CONSENSUS PIPELINE...\n")

        # =========================
        # MEMORY CORE
        # =========================
        self.memory = get_crdt()

        # =========================
        # NETWORK CONFIG
        # =========================
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # MUST MATCH EMITTER EXACTLY
        self.sock.bind((self.host, self.port))

        # =========================
        # STATE ENGINE
        # =========================
        self.running = True
        self.event_count = 0
        self.dropped_packets = 0

        # 🧠 V4 NEW: dedup + ordering
        self.seen_hashes = set()
        self.event_queue = deque(maxlen=1000)

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()
        threading.Thread(target=self.queue_processor_loop, daemon=True).start()

        print(f"\n🟢 [SWARM BUS V4] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # HASHING (DEDUP CORE)
    # =====================================================
    def hash_event(self, event):
        try:
            return str(hash(json.dumps(event, sort_keys=True)))
        except Exception:
            return str(time.time())

    # =====================================================
    # NORMALIZE EVENT
    # =====================================================
    def normalize_event(self, event):
        return {
            "type": event.get("type", "unknown"),
            "content": event.get("content", ""),
            "node_id": event.get("node_id", "external"),
            "timestamp": event.get("timestamp", time.time()),
            "received_at": time.time(),
            "version": "v4"
        }

    # =====================================================
    # MEMORY WRITE (SAFE)
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V4 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V4] LISTENING...\n")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)

                try:
                    event = json.loads(data.decode("utf-8"))
                except Exception:
                    self.dropped_packets += 1
                    continue

                event = self.normalize_event(event)

                # =========================
                # V4 DEDUP SYSTEM
                # =========================
                h = self.hash_event(event)
                if h in self.seen_hashes:
                    continue

                self.seen_hashes.add(h)

                # push into ordered queue
                self.event_queue.append(event)

                print(f"[V4 RX] {event}")

            except Exception as e:
                print("[V4 LISTENER ERROR]", e)
                traceback.print_exc()
                time.sleep(1)

    # =====================================================
    # QUEUE PROCESSOR (ORDERED STREAM)
    # =====================================================
    def queue_processor_loop(self):
        while self.running:
            try:
                if self.event_queue:
                    event = self.event_queue.popleft()

                    self.event_count += 1

                    print(f"[V4 PROCESS] #{self.event_count} -> {event}")

                    self.write_memory(event)

                time.sleep(0.01)

            except Exception as e:
                print("[V4 PROCESS ERROR]", e)

    # =====================================================
    # HEALTH MONITOR
    # =====================================================
    def health_loop(self):
        while self.running:
            try:
                time.sleep(5)

                print("\n🟡 [SWARM BUS V4 STATUS]")
                print(f"  events_processed : {self.event_count}")
                print(f"  dropped_packets  : {self.dropped_packets}")
                print(f"  queue_size       : {len(self.event_queue)}")
                print(f"  memory_events    : {len(self.memory.state.get('events', []))}")
                print("──────────────────────────────\n")

            except Exception as e:
                print("[V4 HEALTH ERROR]", e)

    # =====================================================
    # STOP
    # =====================================================
    def stop(self):
        self.running = False
        self.sock.close()


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    print("""
========================================
🧠 SWARM BUS V4
========================================
✔ UDP LISTENER: 0.0.0.0:6100
✔ DEDUP ENABLED
✔ ORDERED EVENT QUEUE
✔ CRDT MEMORY WRITE
✔ EMITTER MUST MATCH PORT EXACTLY
========================================
""")

    bus = SwarmBusV4()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V4] SHUTDOWN")
        bus.stop()
