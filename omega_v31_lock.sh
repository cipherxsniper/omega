LOCKFILE="/tmp/omega_v31.lock"

if [ -f "$LOCKFILE" ]; then
  echo "⚠️ Omega already starting/running"
  exit 1
fi

echo $$ > "$LOCKFILE"

cleanup() {
  rm -f "$LOCKFILE"
}

trap cleanup EXIT
