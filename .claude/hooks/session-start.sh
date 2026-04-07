#!/bin/bash
# Session Start Hook
# Loads context from Obsidian vault (the real brain) + operational memory

OBSIDIAN="/mnt/c/Users/jacks/OneDrive/Desktop/Project_P/Claude-Brain"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$HOME/jpate")"
TODAY=$(date +%Y-%m-%d)

echo "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
echo "SESSION START \u2014 $(date '+%A, %B %d %Y %I:%M %p')"
echo "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
echo ""

# ── OBSIDIAN BRAIN ──────────────────────────────────────────
if [ -d "$OBSIDIAN" ]; then
  echo "=== OBSIDIAN BRAIN ==="
  for f in "$OBSIDIAN"/0*.md; do
    [ -f "$f" ] && echo "--- $(basename $f) ---" && cat "$f" && echo ""
  done
else
  echo "[WARNING] Obsidian vault not found at: $OBSIDIAN"
  echo "Make sure you are running from WSL and OneDrive is synced."
  echo ""
fi

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
