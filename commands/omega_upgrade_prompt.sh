#!/bin/bash
# ==========================================
# OmegaOS Prompt Upgrade - Dynamic Metrics
# ==========================================

PROJECT_DIR=~/Omega-President/Omega-President
LOGS_DIR="$PROJECT_DIR/logs"
NODES_FILE="$PROJECT_DIR/nodes.json"

# Colors
PURPLE="\[\033[1;35m\]"
CYAN="\[\033[1;36m\]"
GREEN="\[\033[1;32m\]"
YELLOW="\[\033[1;33m\]"
RESET="\[\033[0m\]"

# Function to read brain status
get_brain_state() {
    # Example: always active for now
    echo "active"
}

# Function to count nodes
get_node_count() {
    [[ -f "$NODES_FILE" ]] && jq '.nodes | length' "$NODES_FILE" || echo 0
}

# Function to get CPU load (simple approximation)
get_cpu_load() {
    awk '{u=$2+$4; t=$2+$4+$5; if(t>0) print int(u/t*100); else print 0}' <(grep 'cpu ' /proc/stat) 
}

# Function to get memory usage
get_mem_usage() {
    free -h | awk '/Mem:/ {print $3 "/" $2}'
}

# Write dynamic PS1 into omega_shell.sh
cat << 'EOF' > ~/Omega-President/Omega-President/omega_shell.sh
#!/bin/bash
PROJECT_DIR=~/Omega-President/Omega-President
COMMANDS_DIR="$PROJECT_DIR/commands"

PURPLE="\[\033[1;35m\]"
CYAN="\[\033[1;36m\]"
GREEN="\[\033[1;32m\]"
YELLOW="\[\033[1;33m\]"
RESET="\[\033[0m\]"

get_commands() {
    ls "$COMMANDS_DIR"/omega_*.sh 2>/dev/null | xargs -n1 basename | sed 's/omega_//;s/.sh//'
}

COMMAND_LIST=$(get_commands)

suggest_command() {
    input=$1
    best_match=""
    best_score=999
    for cmd in $COMMAND_LIST; do
        len_diff=$((${#input} - ${#cmd}))
        score=${len_diff#-}
        for (( i=0; i<${#input} && i<${#cmd}; i++ )); do
            [[ "${input:$i:1}" != "${cmd:$i:1}" ]] && score=$((score+1))
        done
        if (( score < best_score )); then
            best_score=$score
            best_match=$cmd
        fi
    done
    echo "$best_match"
}

_omega_complete() {
    COMPREPLY=($(compgen -W "$(get_commands)" "${COMP_WORDS[1]}"))
}
complete -F _omega_complete omega

echo "======================================"
echo " OmegaOS Native Shell - omega~$"
echo " True Intelligence Mode: ACTIVE"
echo " Metrics log → $PROJECT_DIR/logs/omega_shell_metrics.log"
echo "======================================"

while true; do
    brain_state=$(get_brain_state)
    nodes=$(get_node_count)
    cpu=$(get_cpu_load)
    mem=$(get_mem_usage)

    read -e -p "${PURPLE}omega${CYAN}~$${GREEN} [brain:${brain_state} | nodes:${nodes} | CPU:${cpu}% | MEM:${mem}]${YELLOW} " user_input
    if [[ "$user_input" == "exit" ]]; then
        echo "[OmegaOS] Shutting down shell..."
        break
    fi

    COMMAND_LIST=$(get_commands)

    if [[ -x "$COMMANDS_DIR/omega_$user_input.sh" ]]; then
        bash "$COMMANDS_DIR/omega_$user_input.sh"
        continue
    fi

    case "$user_input" in
        help)
            echo "==== OmegaOS Commands ===="
            for cmd in $COMMAND_LIST; do
                echo " - $cmd"
            done
            echo " - exit"
            ;;
        clear)
            clear
            ;;
        *)
            suggestion=$(suggest_command "$user_input")
            echo "[OmegaOS] Command not found: $user_input"
            [[ -n "$suggestion" ]] && echo "[OmegaOS] Did you mean: $suggestion ?"
            ;;
    esac
done
EOF

chmod +x ~/Omega-President/Omega-President/omega_shell.sh
echo "✅ OmegaOS Native Shell upgraded to dynamic, intelligent metrics version."
