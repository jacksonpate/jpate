#!/bin/bash
# Creates a new project folder with a pre-filled CLAUDE.md
# Usage: ./scripts/new-project.sh "My Project Name"

PROJECT_NAME="${1:-new-project}"
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
PROJECT_DIR="../$PROJECT_SLUG"

if [ -d "$PROJECT_DIR" ]; then
  echo "Directory $PROJECT_DIR already exists."
  exit 1
fi

mkdir -p "$PROJECT_DIR"
cp templates/CLAUDE.md "$PROJECT_DIR/CLAUDE.md"

sed -i "s/\[PROJECT NAME\]/$PROJECT_NAME/g" "$PROJECT_DIR/CLAUDE.md"
sed -i "s/\[DATE\]/$(date +%Y-%m-%d)/g" "$PROJECT_DIR/CLAUDE.md"

echo "[OK] Created $PROJECT_DIR"
echo "[OK] CLAUDE.md template copied"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_DIR"
echo "  git init"
echo "  git remote add origin https://github.com/jacksonpate/$PROJECT_SLUG.git"
