#!/usr/bin/env python3
"""
notion-context.py

Pulls live context from Notion for the session-start hook.
Fetches Mind Vault, Task Manager, and Academic Hub via Notion REST API.
Prints formatted output for Claude to read at session start.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError

# Load .env from repo root (script lives in scripts/, env is in root)
load_dotenv(Path(__file__).parent.parent / ".env")

TOKEN = os.getenv("NOTION_TOKEN")
if not TOKEN:
    print("[notion-context] ERROR: NOTION_TOKEN not set in .env")
    sys.exit(1)

notion = Client(auth=TOKEN)

# Page IDs
MIND_VAULT_ID      = "10211b8f-4baf-4d82-9e49-df1b6b9ce22d"
TASK_MANAGER_ID    = "a861e155-0b51-4fe8-a532-344bb1fd0036"
ACADEMIC_HUB_ID    = "a63940ef-0723-49ed-a57e-59771853e745"

DIVIDER = "─" * 50


def rich_text_to_str(rich_text: list) -> str:
    return "".join(rt.get("plain_text", "") for rt in rich_text)


def get_block_children(block_id: str, max_blocks: int = 80) -> list:
    results = []
    cursor = None
    while len(results) < max_blocks:
        kwargs = {"block_id": block_id, "page_size": min(50, max_blocks - len(results))}
        if cursor:
            kwargs["start_cursor"] = cursor
        resp = notion.blocks.children.list(**kwargs)
        results.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return results


def block_to_text(block: dict, indent: int = 0) -> str:
    """Convert a Notion block to plain text."""
    btype = block.get("type", "")
    data = block.get(btype, {})
    prefix = "  " * indent
    text = rich_text_to_str(data.get("rich_text", []))

    if btype == "paragraph":
        return f"{prefix}{text}" if text else ""
    elif btype == "heading_1":
        return f"{prefix}# {text}"
    elif btype == "heading_2":
        return f"{prefix}## {text}"
    elif btype == "heading_3":
        return f"{prefix}### {text}"
    elif btype in ("bulleted_list_item", "numbered_list_item"):
        return f"{prefix}- {text}"
    elif btype == "to_do":
        check = "x" if data.get("checked") else " "
        return f"{prefix}- [{check}] {text}"
    elif btype == "callout":
        icon = data.get("icon", {}).get("emoji", "")
        return f"{prefix}{icon} {text}".strip()
    elif btype == "quote":
        return f"{prefix}> {text}"
    elif btype == "divider":
        return f"{prefix}---"
    elif btype == "code":
        lang = data.get("language", "")
        return f"{prefix}```{lang}\n{prefix}{text}\n{prefix}```"
    elif btype == "child_page":
        title = data.get("title", "")
        return f"{prefix}[page] {title}"
    elif btype == "child_database":
        title = data.get("title", "")
        return f"{prefix}[db] {title}"
    elif btype == "table_row":
        cells = [rich_text_to_str(cell) for cell in data.get("cells", [])]
        return f"{prefix}| " + " | ".join(cells) + " |"
    return ""


def render_page(page_id: str, max_blocks: int = 80) -> list[str]:
    """Render a page's blocks as lines of text."""
    lines = []
    try:
        blocks = get_block_children(page_id, max_blocks)
        for block in blocks:
            line = block_to_text(block)
            if line:
                lines.append(line)
    except APIResponseError as e:
        lines.append(f"[Error reading page: {e}]")
    return lines


def print_section(title: str, lines: list[str]):
    print(f"\n=== {title} ===")
    if lines:
        print("\n".join(lines))
    else:
        print("(empty)")


def fetch_mind_vault():
    lines = render_page(MIND_VAULT_ID, max_blocks=60)
    print_section("MIND VAULT", lines)


def fetch_task_manager():
    lines = render_page(TASK_MANAGER_ID, max_blocks=60)
    print_section("TASK MANAGER", lines)


def fetch_academic_hub():
    lines = render_page(ACADEMIC_HUB_ID, max_blocks=60)
    print_section("ACADEMIC HUB", lines)


def main():
    print(DIVIDER)
    print("NOTION CONTEXT — live pull")
    print(DIVIDER)

    fetch_mind_vault()
    fetch_task_manager()
    fetch_academic_hub()

    print(f"\n{DIVIDER}")


if __name__ == "__main__":
    main()
