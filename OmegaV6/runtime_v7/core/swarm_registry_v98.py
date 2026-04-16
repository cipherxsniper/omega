import json
import time
import threading


class SwarmRegistryV98:
    """
    V9.8 Shared Memory Singleton Swarm Core
    - Single shared memory across ALL swarm modules
    - Peer registry + trust system + memory store
    - Thread-safe (important for your multi-process swarm)
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SwarmRegistryV98, cls).__new__(cls)
                cls._instance._init()
            return cls._instance

    def _init(self):
        self.peers = {}          # peer_id -> ip
        self.trusted = set()     # trusted node IDs
        self.memory = {}         # shared cognitive memory
        self.events = []         # swarm event log
        self.last_seen = {}      # heartbeat tracking

    # ----------------------------
    # 🌐 DISCOVERY LAYER
    # ----------------------------
    def register_peer(self, peer_id, ip):
        self.peers[peer_id] = ip
        self.last_seen[peer_id] = time.time()
        self._log("peer_registered", peer_id)

    # ----------------------------
    # 🔐 TRUST LAYER
    # ----------------------------
    def mark_trusted(self, node_id):
        self.trusted.add(node_id)
        self._log("node_trusted", node_id)

    def is_trusted(self, node_id):
        return node_id in self.trusted

    # ----------------------------
    # 🧠 MEMORY LAYER (V9 CORE)
    # ----------------------------
    def write_memory(self, key, value):
        self.memory[key] = {
            "value": value,
            "timestamp": time.time()
        }

    def read_memory(self, key, default=None):
        return self.memory.get(key, {}).get("value", default)

    def sync_memory(self, incoming_memory: dict):
        for k, v in incoming_memory.items():
            self.memory[k] = v

    # ----------------------------
    # 📡 HEARTBEAT / HEALTH
    # ----------------------------
    def update_heartbeat(self, node_id):
        self.last_seen[node_id] = time.time()

    def get_alive_peers(self, timeout=30):
        now = time.time()
        return [
            pid for pid, ts in self.last_seen.items()
            if now - ts < timeout
        ]

    # ----------------------------
    # 📜 EVENT LOG
    # ----------------------------
    def _log(self, event_type, node_id):
        self.events.append({
            "event": event_type,
            "node_id": node_id,
            "timestamp": time.time()
        })

    def get_events(self):
        return self.events[-50:]  # last 50 events

    # ----------------------------
    # 🧭 DEBUG SNAPSHOT
    # ----------------------------
    def snapshot(self):
        return {
            "peers": len(self.peers),
            "trusted": len(self.trusted),
            "memory_keys": len(self.memory),
            "alive_peers": len(self.get_alive_peers())
        }


# Singleton accessor (IMPORTANT for swarm consistency)
def get_registry():
    return SwarmRegistryV98()
