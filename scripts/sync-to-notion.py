#!/usr/bin/env python3
"""
Notion Sync Script

Watches notes/inbox/ and pushes files to the right Notion database
based on filename prefix.

File naming conventions:
  school-[title].md    -> School Notes database
  journal-[title].md   -> Journal database
  thought-[title].md   -> Quick Capture database
  mind-[title].md      -> Quick Capture database

Setup:
  1. Copy .env.example to .env and fill in your Notion credentials
  2. Run: pip install notion-client python-dotenv
  3. Run: python scripts/sync-to-notion.py
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

try:
    from notion_client import Client
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependencies. Run: pip install notion-client python-dotenv")
    sys.exit(1)

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DB_SCHOOL = os.getenv("NOTION_DB_SCHOOL")
DB_JOURNAL = os.getenv("NOTION_DB_JOURNAL")
DB_QUICK_CAPTURE = os.getenv("NOTION_DB_QUICK_CAPTURE")

INBOX = Path("notes/inbox")
SYNCED = Path("notes/synced")
SYNCED.mkdir(parents=True, exist_ok=True)


def get_database_for_file(filename: str) -> tuple:
    """Returns (database_id, note_type) based on filename prefix."""
    name = filename.lower()
    if name.startswith("school-"):
        return DB_SCHOOL, "School Note"
    elif name.startswith("journal-"):
        return DB_JOURNAL, "Journal"
    elif name.startswith("thought-") or name.startswith("mind-"):
        return DB_QUICK_CAPTURE, "Quick Capture"
    else:
        return DB_QUICK_CAPTURE, "Quick Capture"


def parse_title(filename: str) -> str:
    """Extract readable title from filename."""
    name = Path(filename).stem
    for prefix in ["school-", "journal-", "thought-", "mind-"]:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name.replace("-", " ").replace("_", " ").title()


def sync_file(filepath: Path, notion: Client) -> bool:
    """Push a single markdown file to the appropriate Notion database."""
    filename = filepath.name
    content = filepath.read_text(encoding="utf-8")
    db_id, note_type = get_database_for_file(filename)
    title = parse_title(filename)

    if not db_id:
        print(f"  WARNING: No database configured for: {filename} — add to .env")
        return False

    print(f"  -> Syncing '{title}' to Notion [{note_type}]...")

    notion.pages.create(
        parent={"database_id": db_id},
        properties={
            "Name": {
                "title": [{"text": {"content": title}}]
            },
            "Type": {
                "select": {"name": note_type}
            },
            "Date": {
                "date": {"start": datetime.now().isoformat()}
            }
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content[:2000]}}]
                }
            }
        ]
    )
    return True


def main():
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set in .env")
        sys.exit(1)

    notion = Client(auth=NOTION_TOKEN)
    files = list(INBOX.glob("*.md"))

    if not files:
        print("No files in notes/inbox/ to sync.")
        return

    print(f"Found {len(files)} file(s) to sync...\n")
    synced = 0

    for f in files:
        try:
            success = sync_file(f, notion)
            if success:
                dest = SYNCED / f.name
                shutil.move(str(f), str(dest))
                print(f"  Moved to notes/synced/\n")
                synced += 1
        except Exception as e:
            print(f"  Failed to sync {f.name}: {e}\n")

    print(f"Done. {synced}/{len(files)} files synced to Notion.")


if __name__ == "__main__":
    main()
