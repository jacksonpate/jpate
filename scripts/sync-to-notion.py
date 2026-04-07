#!/usr/bin/env python3
"""
Notion Sync Script — JPATE Agent

School notes  → subpages inside the correct course page
Journal       → Journal database (Mind Vault)
Thought/Mind  → Quick Capture database (Task Manager)

File naming:
  school-[course]-[title].md
    e.g. school-nursing2030-cardiac-output.md
    e.g. school-microbio-gram-staining.md
    e.g. school-microlab-lab6-notes.md
  journal-[title].md
  thought-[title].md  /  mind-[title].md

Setup:
  pip install notion-client python-dotenv
  Fill in .env
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

NOTION_TOKEN     = os.getenv("NOTION_TOKEN")
DB_JOURNAL       = os.getenv("NOTION_DB_JOURNAL")
DB_QUICK_CAPTURE = os.getenv("NOTION_DB_QUICK_CAPTURE")

# Course name → Notion page ID
COURSE_PAGES = {
    "nursing2030": "ae3d9ad3-d831-41c6-a9e5-6e36fe000d42",
    "nurs2030":    "ae3d9ad3-d831-41c6-a9e5-6e36fe000d42",
    "nursing2040": "c9511e78-5e08-41ee-b9ef-8f34c47515d9",
    "nurs2040":    "c9511e78-5e08-41ee-b9ef-8f34c47515d9",
    "microbio":    "be4e4500-5934-493f-88b6-ddfa03113674",
    "microlab":    "be4e4500-5934-493f-88b6-ddfa03113674",
    "micro":       "be4e4500-5934-493f-88b6-ddfa03113674",
}

COURSE_LABELS = {
    "nursing2030": "NURS 2030",
    "nurs2030":    "NURS 2030",
    "nursing2040": "NURS 2040",
    "nurs2040":    "NURS 2040",
    "microbio":    "Microbiology",
    "microlab":    "Micro Lab",
    "micro":       "Microbiology",
}

INBOX  = Path("notes/inbox")
SYNCED = Path("notes/synced")
SYNCED.mkdir(parents=True, exist_ok=True)


# ── Markdown → Notion blocks ──────────────────────────────────────────────

def rich(text: str) -> list:
    """Parse inline **bold** and `code` into Notion rich_text."""
    out, last = [], 0
    for m in re.finditer(r'(\*\*(.+?)\*\*|`(.+?)`)', text):
        if m.start() > last:
            out.append({"type": "text", "text": {"content": text[last:m.start()]}})
        if m.group(2):
            out.append({"type": "text", "text": {"content": m.group(2)}, "annotations": {"bold": True}})
        elif m.group(3):
            out.append({"type": "text", "text": {"content": m.group(3)}, "annotations": {"code": True}})
        last = m.end()
    if last < len(text):
        out.append({"type": "text", "text": {"content": text[last:]}})
    return out or [{"type": "text", "text": {"content": text}}]


def md_to_blocks(content: str) -> list:
    blocks, i = [], 0
    lines = content.split("\n")
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            lang = stripped[3:].strip() or "plain text"
            code, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i += 1
            blocks.append({"object": "block", "type": "code",
                           "code": {"rich_text": [{"type": "text", "text": {"content": "\n".join(code)}}],
                                    "language": lang}})
        elif re.match(r'^[-*_]{3,}$', stripped):
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        elif line.startswith("### "):
            blocks.append({"object": "block", "type": "heading_3", "heading_3": {"rich_text": rich(line[4:])}})
        elif line.startswith("## "):
            blocks.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": rich(line[3:])}})
        elif line.startswith("# "):
            blocks.append({"object": "block", "type": "heading_1", "heading_1": {"rich_text": rich(line[2:])}})
        elif line.startswith("> "):
            blocks.append({"object": "block", "type": "quote", "quote": {"rich_text": rich(line[2:])}})
        elif re.match(r'^- \[(x| )\] ', line):
            checked = line[3] == 'x'
            blocks.append({"object": "block", "type": "to_do",
                           "to_do": {"rich_text": rich(line[6:]), "checked": checked}})
        elif re.match(r'^[-*] ', line):
            blocks.append({"object": "block", "type": "bulleted_list_item",
                           "bulleted_list_item": {"rich_text": rich(line[2:])}})
        elif re.match(r'^\d+\. ', line):
            blocks.append({"object": "block", "type": "numbered_list_item",
                           "numbered_list_item": {"rich_text": rich(re.sub(r'^\d+\. ', '', line))}})
        elif stripped == "":
            pass
        else:
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": rich(line)}})
        i += 1
    return blocks


# ── File parser ────────────────────────────────────────────────────────────

class NoteFile:
    def __init__(self, path: Path):
        self.path    = path
        self.content = path.read_text(encoding="utf-8").strip()
        parts        = path.stem.split("-")
        prefix       = parts[0].lower()

        if prefix == "school" and len(parts) >= 2:
            course_key       = parts[1].lower()
            self.type        = "school"
            self.course_key  = course_key
            self.course_label = COURSE_LABELS.get(course_key, parts[1].title())
            self.page_id     = COURSE_PAGES.get(course_key)
            raw_title        = " ".join(parts[2:]) if len(parts) > 2 else "Notes"
            self.title       = raw_title.replace("-", " ").title()

        elif prefix == "journal":
            self.type   = "journal"
            self.db_id  = DB_JOURNAL
            raw_title   = " ".join(parts[1:]) if len(parts) > 1 else datetime.now().strftime("%B %d %Y")
            self.title  = raw_title.replace("-", " ").title()

        else:  # thought / mind / anything else
            self.type   = "capture"
            self.db_id  = DB_QUICK_CAPTURE
            raw_title   = " ".join(parts[1:]) if len(parts) > 1 else path.stem.replace("-", " ").title()
            self.title  = raw_title.replace("-", " ").title()


# ── Page builders ───────────────────────────────────────────────────────────

def build_school_page(note: NoteFile, notion: Client):
    """Create a subpage inside the course page."""
    now   = datetime.now().strftime("%B %d, %Y  ·  %I:%M %p")
    title = f"\U0001f4da  {note.title}"

    children = [
        # Header callout matching his aesthetic
        {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": f"{note.course_label}  ·  {now}"},
                    "annotations": {"bold": True}
                }],
                "icon": {"emoji": "\U0001f4da"},
                "color": "blue_background"
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
    ]
    children.extend(md_to_blocks(note.content))

    notion.pages.create(
        parent={"page_id": note.page_id},
        icon={"emoji": "\U0001f4da"},
        properties={"title": [{"text": {"content": title}}]},
        children=children
    )


def build_journal_page(note: NoteFile, notion: Client):
    """Create an entry in the Journal database."""
    now = datetime.now().strftime("%B %d, %Y  ·  %I:%M %p")
    children = [
        {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": now}, "annotations": {"bold": True}}],
                "icon": {"emoji": "\U0001f4d3"},
                "color": "purple_background"
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
    ]
    children.extend(md_to_blocks(note.content))

    notion.pages.create(
        parent={"database_id": note.db_id},
        icon={"emoji": "\U0001f4d3"},
        properties={
            "Name": {"title": [{"text": {"content": note.title}}]},
            "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        },
        children=children
    )


def build_capture_page(note: NoteFile, notion: Client):
    """Create an entry in the Quick Capture database."""
    now = datetime.now().strftime("%B %d, %Y  ·  %I:%M %p")
    children = [
        {
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": now}, "annotations": {"bold": True}}],
                "icon": {"emoji": "\u26a1"},
                "color": "yellow_background"
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
    ]
    children.extend(md_to_blocks(note.content))

    notion.pages.create(
        parent={"database_id": note.db_id},
        icon={"emoji": "\u26a1"},
        properties={
            "Name": {"title": [{"text": {"content": note.title}}]},
            "Date": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        },
        children=children
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def sync_file(note: NoteFile, notion: Client) -> bool:
    if note.type == "school":
        if not note.page_id:
            print(f"  WARNING: No page ID for course '{note.course_key}' — add to COURSE_PAGES in script")
            return False
        print(f"  \U0001f4da  {note.course_label}  →  {note.title}")
        build_school_page(note, notion)

    elif note.type == "journal":
        if not note.db_id:
            print(f"  WARNING: NOTION_DB_JOURNAL not set in .env")
            return False
        print(f"  \U0001f4d3  Journal  →  {note.title}")
        build_journal_page(note, notion)

    else:
        if not note.db_id:
            print(f"  WARNING: NOTION_DB_QUICK_CAPTURE not set in .env")
            return False
        print(f"  \u26a1  Quick Capture  →  {note.title}")
        build_capture_page(note, notion)

    return True


def main():
    if not NOTION_TOKEN:
        print("Error: NOTION_TOKEN not set in .env")
        sys.exit(1)

    notion = Client(auth=NOTION_TOKEN)
    files  = list(INBOX.glob("*.md"))

    if not files:
        print("No files in notes/inbox/ to sync.")
        return

    print(f"Syncing {len(files)} file(s)...\n")
    synced = 0

    for fp in files:
        try:
            note = NoteFile(fp)
            if sync_file(note, notion):
                shutil.move(str(fp), str(SYNCED / fp.name))
                print(f"      \u2713 Done\n")
                synced += 1
        except Exception as e:
            print(f"      \u2717 Failed ({fp.name}): {e}\n")

    print(f"Complete. {synced}/{len(files)} synced.")


if __name__ == "__main__":
    main()
