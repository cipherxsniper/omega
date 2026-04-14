from queue import Queue
import threading

WRITE_QUEUE = Queue()

def start_writer_loop(self):
    while True:
        graph = WRITE_QUEUE.get()
        self._atomic_write(graph)

def enqueue_write(graph):
    WRITE_QUEUE.put(graph)
