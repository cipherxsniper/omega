#!/data/data/com.termux/files/usr/bin/bash

# ===============================
# OMEGA GIT INTELLIGENCE v7
# EVOLUTIONARY SYSTEM BRAIN
# ===============================

WATCH_DIR="$HOME/Omega"
cd "$WATCH_DIR" || exit

GEN_FILE=".omega_generation"
STATE_FILE=".omega_git_state"

echo "🧠 OMEGA GIT INTELLIGENCE v7 ONLINE"
echo "------------------------------------"

# init generation
if [ ! -f "$GEN_FILE" ]; then
    echo 1 > "$GEN_FILE"
fi

get_gen() {
    cat "$GEN_FILE"
}

increment_gen() {
    GEN=$(get_gen)
    GEN=$((GEN + 1))
    echo $GEN > "$GEN_FILE"
}

classify_changes() {

    CORE=$(git diff --cached --name-only | grep -E "omega_kernel|core|brain|orchestrator" | wc -l)
    MEMORY=$(git diff --cached --name-only | grep -E "memory|json" | wc -l)
    MODULE=$(git diff --cached --name-only | grep -E "engine|bus|node|swarm" | wc -l)
    EXPERIMENT=$(git diff --cached --name-only | grep -E "v[0-9]+|test|experimental" | wc -l)

    echo "$CORE $MODULE $MEMORY $EXPERIMENT"
}

should_block() {
    if git diff --cached --quiet; then
        echo "1"
        return
    fi

    if git diff --cached --name-only | grep -q "_dist/"; then
        echo "1"
        return
    fi

    echo "0"
}

commit_evolution() {

    GEN=$(get_gen)

    read CORE MODULE MEMORY EXPERIMENT <<< $(classify_changes)

    TAG="GEN-$GEN"

    echo "🧠 Classifying evolution:"
    echo "CORE=$CORE MODULE=$MODULE MEMORY=$MEMORY EXP=$EXPERIMENT"

    MSG="[OMEGA $TAG] "

    if [ "$CORE" -gt 0 ]; then
        MSG+="CORE_EVOLUTION "
    fi

    if [ "$MODULE" -gt 0 ]; then
        MSG+="MODULE_EXPANSION "
    fi

    if [ "$MEMORY" -gt 0 ]; then
        MSG+="MEMORY_SYNC "
    fi

    if [ "$EXPERIMENT" -gt 0 ]; then
        MSG+="EXPERIMENTAL_PATCH "
    fi

    MSG+="| $(date '+%Y-%m-%d %H:%M:%S')"

    git add -A

    if should_block; then
        echo "🛑 Safety gate blocked unsafe commit"
        return
    fi

    if git diff --cached --quiet; then
        echo "🟡 No evolutionary change detected"
        return
    fi

    echo "🧬 Committing evolution:"
    echo "$MSG"

    git commit -m "$MSG"

    echo "🚀 Pushing evolution..."
    git push

    increment_gen

    echo "✅ Evolution complete → GEN $GEN"
}

# ===============================
# WATCH LOOP
# ===============================

while true; do

    inotifywait -r -e modify,create,delete,move "$WATCH_DIR" >/dev/null 2>&1

    sleep 2

    commit_evolution

done
