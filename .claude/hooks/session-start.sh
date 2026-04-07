#!/bin/bash
# Session Start Hook — runs when Claude Code starts a session
# Output is injected into Claude's context automatically

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ".")"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SESSION START — $(date '+%A, %B %d %Y %I:%M %p')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Load master context
if [ -f "$REPO_ROOT/CLAUDE.md" ]; then
  echo "=== MASTER CONTEXT ==="
  cat "$REPO_ROOT/CLAUDE.md"
  echo ""
fi

# Load personal context
if [ -f "$REPO_ROOT/memory/personal-context.md" ]; then
  echo "=== PERSONAL CONTEXT ==="
  cat "$REPO_ROOT/memory/personal-context.md"
  echo ""
fi

# Load project status
if [ -f "$REPO_ROOT/memory/projects.md" ]; then
  echo "=== PROJECT STATUS ==="
  cat "$REPO_ROOT/memory/projects.md"
  echo ""
fi

# Load shared agent memory
if [ -f "$REPO_ROOT/memory/shared-memory.md" ]; then
  echo "=== SHARED AGENT MEMORY ==="
  cat "$REPO_ROOT/memory/shared-memory.md"
  echo ""
fi

# Show today's log if it exists
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$REPO_ROOT/memory/daily-log/$TODAY.md"
if [ -f "$LOG_FILE" ]; then
  echo "=== TODAY'S LOG ==="
  cat "$LOG_FILE"
  echo ""
fi

# Check for notes waiting to sync to Notion
INBOX_COUNT=$(ls "$REPO_ROOT/notes/inbox/"*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$INBOX_COUNT" -gt "0" ]; then
  echo "⚠  $INBOX_COUNT note(s) in inbox waiting to sync to Notion"
  echo "   Run: python scripts/sync-to-notion.py"
  echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ready. What are we working on today?"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
