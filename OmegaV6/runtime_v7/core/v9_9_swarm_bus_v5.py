import socket
import json
import time
import threading
import traceback
import hashlib
import hmac
from collections import deque, defaultdict

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV5:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠⚙️ [SWARM BUS V5] INITIALIZING CONSENSUS + TRUST NETWORK...\n")

        # =========================
        # MEMORY CORE (CRDT)
        # =========================
        self.memory = get_crdt()

        # =========================
        # NETWORK
        # =========================
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        # =========================
        # SECURITY
        # =========================
        self.secret = b"omega-swarm-v5-trust-key"

        # =========================
        # STATE
        # =========================
        self.running = True
        self.event_count = 0

        # 🧠 V5: trust system
        self.trust = defaultdict(lambda: 1.0)

        # 🧠 V5: ACK tracking
        self.pending_acks = {}
        self.retry_queue = deque()

        # =========================
        # EVENT PIPELINE
        # =========================
        self.event_queue = deque(maxlen=5000)

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.retry_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()

        print(f"🟢 [SWARM BUS V5] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # SECURITY (NODE AUTH)
    # =====================================================
    def verify_signature(self, event):
        try:
            sig = event.get("signature")
            raw = json.dumps({k: event[k] for k in event if k != "signature"}, sort_keys=True).encode()

            expected = hmac.new(self.secret, raw, hashlib.sha256).hexdigest()

            return hmac.compare_digest(sig, expected)

        except Exception:
            return False

    # =====================================================
    # EVENT ID
    # =====================================================
    def event_id(self, event):
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # =====================================================
    # TRUST UPDATE
    # =====================================================
    def update_trust(self, node_id, success=True):
        if success:
            self.trust[node_id] += 0.01
        else:
            self.trust[node_id] -= 0.05

        # clamp
        self.trust[node_id] = max(0.1, min(5.0, self.trust[node_id]))

    # =====================================================
    # MEMORY WRITE (CRDT SAFE)
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V5 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V5] LISTENING...\n")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)

                try:
                    event = json.loads(data.decode())
                except Exception:
                    continue

                # =========================
                # AUTH CHECK
                # =========================
                if not self.verify_signature(event):
                    self.update_trust(event.get("node_id", "unknown"), success=False)
                    continue

                eid = self.event_id(event)
                event["event_id"] = eid
                event["received_at"] = time.time()

                # enqueue
                self.event_queue.append(event)

            except Exception:
                traceback.print_exc()
                time.sleep(1)

    # =====================================================
    # PROCESSOR (CONSENSUS CORE)
    # =====================================================
    def processor_loop(self):
        while self.running:
            try:
                if self.event_queue:
                    event = self.event_queue.popleft()

                    node = event.get("node_id", "unknown")

                    self.event_count += 1

                    print(f"[V5 EVENT] #{self.event_count} from {node} -> {event}")

                    # store in CRDT memory
                    self.write_memory(event)

                    # register ACK requirement
                    self.pending_acks[event["event_id"]] = {
                        "event": event,
                        "time": time.time(),
                        "attempts": 0
                    }

                    self.update_trust(node, success=True)

                time.sleep(0.01)

            except Exception as e:
                print("[V5 PROCESS ERROR]", e)

    # =====================================================
    # RETRY SYSTEM
    # =====================================================
    def retry_loop(self):
        while self.running:
            try:
                now = time.time()

                for eid, data in list(self.pending_acks.items()):
                    if now - data["time"] > 3:
                        data["attempts"] += 1
                        data["time"] = now

                        print(f"[V5 RETRY] event {eid} attempt {data['attempts']}")

                        # too many retries → penalize trust
                        if data["attempts"] > 3:
                            node = data["event"].get("node_id", "unknown")
                            self.update_trust(node, success=False)
                            del self.pending_acks[eid]

                time.sleep(2)

            except Exception as e:
                print("[V5 RETRY ERROR]", e)

    # =====================================================
    # HEALTH
    # =====================================================
    def health_loop(self):
        while self.running:
            time.sleep(5)

            print("\n🟡 [SWARM BUS V5 STATUS]")
            print(f"  events_processed : {self.event_count}")
            print(f"  pending_acks     : {len(self.pending_acks)}")
            print(f"  queue_size       : {len(self.event_queue)}")
            print(f"  trust_snapshot   : {dict(self.trust)}")
            print(f"  memory_events    : {len(self.memory.state.get('events', []))}")
            print("──────────────────────────────\n")

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
🧠 SWARM BUS V5 — CONSENSUS SYSTEM
========================================
✔ NODE AUTH (HMAC)
✔ ACK TRACKING
✔ RETRY SYSTEM
✔ TRUST SCORING
✔ CRDT MEMORY MERGE
✔ UDP: 0.0.0.0:6100
========================================
""")

    bus = SwarmBusV5()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V5] SHUTDOWN")
        bus.stop()
