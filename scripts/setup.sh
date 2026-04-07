#!/bin/bash
# One-time setup script for Jackson's supersystem
# Run this from your home machine after cloning the repo

set -e

echo "Setting up Jackson's supersystem..."
echo ""

# 1. Copy .env.example to .env
if [ ! -f .env ]; then
  cp .env.example .env
  echo "[OK] Created .env - fill in your API keys"
else
  echo "[OK] .env already exists"
fi

# 2. Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install notion-client python-dotenv 2>/dev/null || pip3 install notion-client python-dotenv
echo "[OK] Python dependencies installed"

# 3. Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x .claude/hooks/*.sh 2>/dev/null || true
echo "[OK] Scripts made executable"

# 4. Create directories
mkdir -p notes/inbox notes/synced memory/daily-log
echo "[OK] Directories created"

echo ""
echo "============================================"
echo "Setup complete! Next steps:"
echo ""
echo "1. Fill in .env with your Notion API keys"
echo "2. Fill in CLAUDE.md with your personal context"
echo "3. Fill in memory/personal-context.md"
echo "4. Add your projects to memory/projects.md"
echo "5. Copy .claude/settings.json to ~/.claude/settings.json"
echo "============================================"
