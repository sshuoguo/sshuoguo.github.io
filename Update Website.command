#!/bin/zsh
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$PROJECT_DIR/website-update.log"
cd "$PROJECT_DIR" || exit 1

if python3 scripts/render_site.py >"$LOG_FILE" 2>&1; then
  open "$LOG_FILE"
else
  open "$LOG_FILE"
  exit 1
fi
