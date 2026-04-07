#!/bin/bash
# Session Start Hook
# Loads context from Obsidian vault (the real brain) + operational memory

REPO_ROOT="/c/Users/jacks/OneDrive/Desktop/jpate"
TODAY=$(date +%Y-%m-%d)
PYTHON="/c/Users/jacks/AppData/Local/Python/bin/python3"

echo "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
echo "SESSION START \u2014 $(date '+%A, %B %d %Y %I:%M %p')"
echo "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
echo ""

# ── NOTION LIVE CONTEXT ─────────────────────────────────────
if [ -f "$REPO_ROOT/scripts/notion-context.py" ]; then
  PYTHONUTF8=1 "$PYTHON" "$REPO_ROOT/scripts/notion-context.py" 2>/dev/null || \
    echo "[WARNING] Notion context pull failed — check NOTION_TOKEN in .env"
else
  echo "[WARNING] notion-context.py not found at $REPO_ROOT/scripts/"
fi
echo ""

# ── OPERATIONAL MEMORY ──────────────────────────────────────
if [ -f "$REPO_ROOT/memory/projects.md" ]; then
  echo "=== ACTIVE PROJECTS ==="
  cat "$REPO_ROOT/memory/projects.md"
  echo ""
fi

if [ -f "$REPO_ROOT/memory/shared-memory.md" ]; then
  echo "=== AGENT SHARED MEMORY ==="
  cat "$REPO_ROOT/memory/shared-memory.md"
  echo ""
fi

# ── TODAY'S LOG ─────────────────────────────────────────────
LOG_FILE="$REPO_ROOT/memory/daily-log/$TODAY.md"
if [ -f "$LOG_FILE" ]; then
  echo "=== TODAY'S LOG ==="
  cat "$LOG_FILE"
  echo ""
fi

# ── INBOX CHECK ─────────────────────────────────────────────
INBOX_COUNT=$(ls "$REPO_ROOT/notes/inbox/"*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$INBOX_COUNT" -gt "0" ]; then
  echo "\u26a0  $INBOX_COUNT note(s) in inbox waiting to sync to Notion"
  echo "   Run: python scripts/sync-to-notion.py"
  echo ""
fi

echo "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
echo "Ready."
echo "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
