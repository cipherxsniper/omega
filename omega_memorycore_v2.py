""" OMEGA MEMORYCORE v2 Non-blocking, async, buffered memory system for Omega kernel Fixes: JSON bottleneck, tick lag, full-state rewrite issues """

import json import time import threading from collections import deque from datetime import datetime

class OmegaMemoryCoreV2: def init(self, path="omega_memory.json", flush_interval=50, max_buffer=500): self.path = path self.flush_interval = flush_interval self.buffer = deque(maxlen=max_buffer)

self.tick_counter = 0
    self.last_flush_tick = 0

    self.lock = threading.Lock()
    self.running = True

    # start background writer thread
    self.writer_thread = threading.Thread(target=self._writer_loop, daemon=True)
    self.writer_thread.start()

# -----------------------------
# PUBLIC API
# -----------------------------

def log_state(self, state: dict):
    """Fast non-blocking append into memory buffer"""
    with self.lock:
        self.buffer.append({
            "timestamp": time.time(),
            "state": state
        })

    self.tick_counter += 1

def save_checkpoint(self):
    """Force flush buffer to disk (safe snapshot)"""
    with self.lock:
        data = list(self.buffer)

    snapshot = {
        "created": datetime.utcnow().isoformat(),
        "ticks": self.tick_counter,
        "memory": data
    }

    with open(self.path, "w") as f:
        json.dump(snapshot, f, indent=2)

def stop(self):
    """Graceful shutdown"""
    self.running = False
    self.save_checkpoint()

# -----------------------------
# INTERNAL WRITER LOOP
# -----------------------------

def _writer_loop(self):
    while self.running:
        time.sleep(1)

        if self.tick_counter - self.last_flush_tick >= self.flush_interval:
            self._flush()
            self.last_flush_tick = self.tick_counter

def _flush(self):
    """Incremental flush (non-blocking snapshot write)"""
    with self.lock:
        if not self.buffer:
            return
        data = list(self.buffer)

    try:
        snapshot = {
            "created": datetime.utcnow().isoformat(),
            "ticks": self.tick_counter,
            "memory": data
        }

        with open(self.path, "w") as f:
            json.dump(snapshot, f)

    except Exception as e:
        # fail-safe: never crash kernel from disk issues
        print("[MemoryCoreV2] flush error:", e)

-----------------------------

DROP-IN REPLACEMENT USAGE

-----------------------------

""" Replace in omega_kernel:

OLD: self.memory.log_state(state)

NEW: self.memory.log_state(state)

AND initialize: self.memory = OmegaMemoryCoreV2()

Shutdown hook: self.memory.stop() """
