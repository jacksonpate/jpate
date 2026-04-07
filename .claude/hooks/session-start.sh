#!/bin/bash
# Session Start Hook
# 1. Obsidian (Project_P/Claude-Brain) — who you are, long-term memory, agent context
# 2. Notion — live priorities, deadlines, active situations
# Falls back to Obsidian-only if Notion is unreachable

REPO_ROOT="/c/Users/jacks/OneDrive/Desktop/jpate"
OBSIDIAN="/c/Users/jacks/OneDrive/Desktop/Project_P/Claude-Brain"
TODAY=$(date +%Y-%m-%d)
PYTHON="/c/Users/jacks/AppData/Local/Python/bin/python3"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SESSION START — $(date '+%A, %B %d %Y %I:%M %p')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── 1. OBSIDIAN BRAIN (identity, memory, deep context) ──────
if [ -d "$OBSIDIAN" ]; then
  echo "=== OBSIDIAN BRAIN ==="
  for f in "$OBSIDIAN"/0*.md; do
    if [ -f "$f" ]; then
      echo ""
      echo "--- $(basename $f) ---"
      cat "$f"
    fi
  done
  echo ""
else
  echo "[WARNING] Obsidian vault not found at: $OBSIDIAN"
  echo ""
fi

# ── 2. AGENT MEMORY (jpate repo memory files) ───────────────
if [ -f "$REPO_ROOT/memory/personal-context.md" ]; then
  echo "=== PERSONAL CONTEXT ==="
  cat "$REPO_ROOT/memory/personal-context.md"
  echo ""
fi

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

# ── 3. TODAY'S LOG ──────────────────────────────────────────
LOG_FILE="$REPO_ROOT/memory/daily-log/$TODAY.md"
if [ -f "$LOG_FILE" ]; then
  echo "=== TODAY'S LOG ==="
  cat "$LOG_FILE"
  echo ""
fi

# ── 4. NOTION LIVE FEED (priorities, deadlines, situations) ─
echo "=== NOTION LIVE FEED ==="
if [ -f "$REPO_ROOT/scripts/notion-context.py" ]; then
  PYTHONUTF8=1 "$PYTHON" "$REPO_ROOT/scripts/notion-context.py" 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "[Notion unreachable — running on Obsidian context only]"
  fi
else
  echo "[notion-context.py not found — running on Obsidian context only]"
fi
echo ""

# ── 5. INBOX CHECK ──────────────────────────────────────────
INBOX_COUNT=$(ls "$REPO_ROOT/notes/inbox/"*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$INBOX_COUNT" -gt "0" ]; then
  echo "⚠  $INBOX_COUNT note(s) in inbox — run: python scripts/sync-to-notion.py"
  echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ready."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
