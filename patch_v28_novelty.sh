#!/bin/bash

FILE="wink_wink_brain_v28.py"

cat >> $FILE << 'INNER'

def global_novelty(sentence):
    recent = get_recent(20)
    overlap = 0

    for s in recent:
        if len(set(sentence.split()) & set(s.split())) > 5:
            overlap += 1

    return 1.0 - min(overlap * 0.2, 1.0)

INNER

echo "novelty function injected"
