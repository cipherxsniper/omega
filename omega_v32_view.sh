#!/bin/bash

tail -F logs/brain.log logs/control.log | grep --line-buffered -E "NODE|AVG|SWARM|tick|MESH|ACTIVE"
