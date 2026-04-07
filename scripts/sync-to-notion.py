#!/usr/bin/env python3
"""
Notion Sync Script — JPATE Agent

Routes notes from notes/inbox/ to the right Notion database with clean,
type-specific formatting. Parses markdown into proper Notion blocks.

File naming:
  school-[course]-[title].md     e.g. school-nursing2030-cardiac-notes.md
  journal-[title].md
  thought-[title].md
  mind-[title].md

Setup:
  pip install notion-client python-dotenv
  Fill in .env with NOTION_TOKEN + database IDs
"""

import os
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime

try:
    from notion_client import Client
    from dotenv import load_dotenv
except ImportError:
    print("Run: pip install notion-client python-dotenv")
    sys.exit(1)

load_dotenv()

NOTION_TOKEN      = os.getenv("NOTION_TOKEN")
DB_SCHOOL         = os.getenv("NOTION_DB_SCHOOL")
DB_JOURNAL        = os.getenv("NOTION_DB_JOURNAL")
DB_QUICK_CAPTURE  = os.getenv("NOTION_DB_QUICK_CAPTURE")

INBOX  = Path("notes/inbox")
SYNCED = Path("notes/synced")
SYNCED.mkdir(parents=True, exist_ok=True)

ICONS = {
    "School Note":     "\U0001f4da",
    "Journal":         "\U0001f4d3",
    "Quick Capture":   "\u26a1",
}


# ─────────────────────────────────────────────────────────────────────────
class FileInfo:
    def __init__(self, path: Path):
        self.path = path
        self.filename = path.name
        self.stem = path.stem
        self.content = path.read_text(encoding="utf-8").strip()
        self._parse()

    def _parse(self):
        parts = self.stem.split("-")
        prefix = parts[0].lower()

        if prefix == "school":
            self.db_id    = DB_SCHOOL
            self.type     = "School Note"
            # school-nursing2030-topic -> course=nursing2030, rest=title
            if len(parts) > 2:
                self.course = parts[1].replace("nursing", "Nursing ").replace("micro", "Micro").title()
                self.title  = " ".join(parts[2:]).replace("-", " ").title()
            else:
                self.course = "General"
                self.title  = " ".join(parts[1:]).replace("-", " ").title() if len(parts) > 1 else self.stem.title()

        elif prefix == "journal":
            self.db_id    = DB_JOURNAL
            self.type     = "Journal"
            self.course   = None
            self.title    = " ".join(parts[1:]).replace("-", " ").title() if len(parts) > 1 else datetime.now().strftime("%B %d, %Y")

        else:  # thought / mind / anything else
            self.db_id    = DB_QUICK_CAPTURE
            self.type     = "Quick Capture"
            self.course   = None
            self.title    = " ".join(parts[1:]).replace("-", " ").title() if len(parts) > 1 else self.stem.replace("-", " ").title()


# ─────────────────────────────────────────────────────────────────────────
def rich(text: str) -> list:
    """Convert a line of text with **bold** and `code` to Notion rich_text array."""
    segments = []
    pattern = re.compile(r'(\*\*(.+?)\*\*|`(.+?)`)')
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            segments.append({"type": "text", "text": {"content": text[last:m.start()]}})
        if m.group(2):  # bold
            segments.append({"type": "text", "text": {"content": m.group(2)}, "annotations": {"bold": True}})
        elif m.group(3):  # code
            segments.append({"type": "text", "text": {"content": m.group(3)}, "annotations": {"code": True}})
        last = m.end()
    if last < len(text):
        segments.append({"type": "text", "text": {"content": text[last:]}})
    return segments if segments else [{"type": "text", "text": {"content": text}}]


def md_to_blocks(content: str) -> list:
    """Parse markdown content into Notion block objects."""
    blocks = []
    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip() or "plain text"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append({
                "object": "block", "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": "\n".join(code_lines)}}],
                    "language": lang
                }
            })

        # Divider
        elif re.match(r'^[-*_]{3,}$', line.strip()):
            blocks.append({"object": "block", "type": "divider", "divider": {}})

        # Headings
        elif line.startswith("### "):
            blocks.append({"object": "block", "type": "heading_3",
                           "heading_3": {"rich_text": rich(line[4:])}})
        elif line.startswith("## "):
            blocks.append({"object": "block", "type": "heading_2",
                           "heading_2": {"rich_text": rich(line[3:])}})
        elif line.startswith("# "):
            blocks.append({"object": "block", "type": "heading_1",
                           "heading_1": {"rich_text": rich(line[2:])}})

        # Blockquote
        elif line.startswith("> "):
            blocks.append({"object": "block", "type": "quote",
                           "quote": {"rich_text": rich(line[2:])}})

        # Checkbox
        elif re.match(r'^- \[(x| )\] ', line):
            checked = line[3] == 'x'
            text = line[6:]
            blocks.append({"object": "block", "type": "to_do",
                           "to_do": {"rich_text": rich(text), "checked": checked}})

        # Bullet
        elif re.match(r'^[-*] ', line):
            blocks.append({"object": "block", "type": "bulleted_list_item",
                           "bulleted_list_item": {"rich_text": rich(line[2:])}})

        # Numbered list
        elif re.match(r'^\d+\. ', line):
            text = re.sub(r'^\d+\. ', '', line)
            blocks.append({"object": "block", "type": "numbered_list_item",
                           "numbered_list_item": {"rich_text": rich(text)}})

        # Blank line
        elif line.strip() == "":
            pass

        # Paragraph
        else:
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": rich(line)}})
        i += 1

    return blocks


# ─────────────────────────────────────────────────────────────────────────
def build_properties(f: FileInfo) -> dict:
    """Build type-specific Notion page properties."""
    base = {
        "Name": {"title": [{"text": {"content": f.title}}]},
        "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        "Type": {"select": {"name": f.type}},
    }
    if f.type == "School Note" and f.course:
        base["Course"] = {"select": {"name": f.course}}
    return base


def build_children(f: FileInfo) -> list:
    """Build the page body with a type-specific header block + parsed content."""
    now = datetime.now().strftime("%B %d, %Y  %I:%M %p")
    children = []

    # Callout header
    if f.type == "School Note":
        header_text = f"Course: {f.course}  \u00b7  {now}"
        color = "blue_background"
    elif f.type == "Journal":
        header_text = now
        color = "purple_background"
    else:
        header_text = now
        color = "yellow_background"

    children.append({
        "object": "block", "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": header_text}}],
            "icon": {"emoji": ICONS[f.type]},
            "color": color
        }
    })

    children.append({"object": "block", "type": "divider", "divider": {}})
    children.extend(md_to_blocks(f.content))
    return children


# ─────────────────────────────────────────────────────────────────────────
def sync_file(filepath: Path, notion: Client) -> bool:
    f = FileInfo(filepath)

    if not f.db_id:
        print(f"  WARNING: No DB configured for {f.type} \u2014 check .env")
        return False

    print(f"  {ICONS[f.type]}  [{f.type}] {f.title}")
    if f.course:
        print(f"      Course: {f.course}")

    notion.pages.create(
        parent={"database_id": f.db_id},
        icon={"emoji": ICONS[f.type]},
        properties=build_properties(f),
        children=build_children(f)
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

    print(f"Syncing {len(files)} file(s) to Notion...\n")
    synced = 0

    for fp in files:
        try:
            if sync_file(fp, notion):
                shutil.move(str(fp), str(SYNCED / fp.name))
                print(f"      \u2713 Done\n")
                synced += 1
        except Exception as e:
            print(f"      \u2717 Failed: {e}\n")

    print(f"Complete. {synced}/{len(files)} synced.")


if __name__ == "__main__":
    main()
