def compute_consensus(nodes):
    if not nodes:
        return 0.0, 1.0

    avg_signal = sum(n["signal"] for n in nodes) / len(nodes)
    avg_instability = sum(n["instability"] for n in nodes) / len(nodes)

    # stability emerges from LOW instability + MID signal
    coherence = max(0.0, min(1.0, avg_signal * (1 - avg_instability)))

    return avg_signal, coherence
