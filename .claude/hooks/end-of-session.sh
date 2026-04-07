#!/bin/bash
# End of Session Hook — auto-commits, pushes, and logs the session

REPO_ROOT="/c/Users/jacks/OneDrive/Desktop/jpate"
TODAY=$(date +%Y-%m-%d)
LOG_DIR="$REPO_ROOT/memory/daily-log"
LOG_FILE="$LOG_DIR/$TODAY.md"

mkdir -p "$LOG_DIR"

# Create or append to today's log
if [ ! -f "$LOG_FILE" ]; then
  echo "# Session Log — $TODAY" > "$LOG_FILE"
  echo "" >> "$LOG_FILE"
fi

echo "## Session ended — $(date '+%I:%M %p')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Auto-commit and push if there are changes
cd "$REPO_ROOT"
if [ -n "$(git status --porcelain)" ]; then
  git add .
  git commit -m "session: auto-save $(date '+%Y-%m-%d %H:%M')"
  git push origin "$(git branch --show-current)" 2>/dev/null || echo "⚠ Push failed — check your connection"
  echo "✓ Changes committed and pushed"
else
  echo "✓ No changes to commit"
fi
