import multiprocessing
import time
from runtime_v7.core.v8_2_swarm_node import SwarmNodeV82


def run_node(port, peers):
    node = SwarmNodeV82(port, peers)
    node.start()

    while True:
        time.sleep(999)


if __name__ == "__main__":
    # define swarm topology
    nodes = [
        (6001, [6002, 6003]),
        (6002, [6001, 6003]),
        (6003, [6001, 6002]),
    ]

    processes = []

    for port, peers in nodes:
        p = multiprocessing.Process(target=run_node, args=(port, peers))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
