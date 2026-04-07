"""Thin wrapper around the Notion API client for the JPATE Triage Agent.

All methods propagate `notion_client.errors.APIResponseError` to callers.
The daemon loop in agent.py is responsible for catching and logging these.
"""
from notion_client import Client

# Name of the Date property in the Notion Calendar DB
_CALENDAR_DATE_PROPERTY = "Date"


def _plain_text(rich_text: list) -> str:
    return "".join(rt.get("plain_text", "") for rt in rich_text)


def _paginate(fn, **kwargs) -> list:
    """Collect all results across paginated Notion API responses (max 50 pages)."""
    results = []
    cursor = None
    for _ in range(50):  # safety cap — prevents infinite loop on API quirks
        resp = fn(**kwargs, start_cursor=cursor) if cursor else fn(**kwargs)
        results.extend(resp["results"])
        if not resp.get("has_more"):
            break
        cursor = resp["next_cursor"]
    return results


class NotionClient:
    def __init__(self, token: str):
        self._client = Client(auth=token)

    def get_child_pages(self, page_id: str) -> list[dict]:
        """Return [{id, title}] for all child_page blocks under page_id."""
        blocks = _paginate(self._client.blocks.children.list, block_id=page_id)
        return [
            {"id": b["id"], "title": b["child_page"]["title"]}
            for b in blocks
            if b["type"] == "child_page"
        ]

    def get_pdf_blocks(self, page_id: str) -> list[dict]:
        """Return [{id, url, name}] for all pdf blocks under page_id."""
        blocks = _paginate(self._client.blocks.children.list, block_id=page_id)
        result = []
        for b in blocks:
            if b["type"] != "pdf":
                continue
            pdf = b["pdf"]
            url = pdf["file"]["url"] if pdf["type"] == "file" else pdf["external"]["url"]
            name = url.split("?")[0].split("/")[-1] or "uploaded.pdf"
            result.append({"id": b["id"], "url": url, "name": name})
        return result

    def get_image_blocks(self, page_id: str) -> list[dict]:
        """Return [{id, url, name}] for all image blocks under page_id."""
        blocks = _paginate(self._client.blocks.children.list, block_id=page_id)
        result = []
        for b in blocks:
            if b["type"] != "image":
                continue
            img = b["image"]
            url = img["file"]["url"] if img["type"] == "file" else img["external"]["url"]
            name = url.split("?")[0].split("/")[-1] or "image"
            result.append({"id": b["id"], "url": url, "name": name})
        return result

    def get_all_blocks(self, page_id: str) -> list[dict]:
        """Return all direct child blocks of a page."""
        return _paginate(self._client.blocks.children.list, block_id=page_id)

    @staticmethod
    def extract_text(blocks: list[dict]) -> str:
        """Extract plain text from a list of Notion blocks."""
        lines = []
        text_types = {
            "paragraph", "heading_1", "heading_2", "heading_3",
            "bulleted_list_item", "numbered_list_item", "to_do",
            "toggle", "quote", "callout",
        }
        for b in blocks:
            btype = b.get("type")
            if btype in text_types and btype in b:
                rt = b[btype].get("rich_text", [])
                text = _plain_text(rt)
                if text:
                    lines.append(text)
        return "\n".join(lines)

    def get_page_text(self, page_id: str) -> str:
        """Fetch all blocks from a page and return as plain text."""
        blocks = self.get_all_blocks(page_id)
        return self.extract_text(blocks)

    def create_child_page(self, parent_id: str, title: str, children: list[dict]) -> str:
        """Create a child page and return its page ID."""
        # Notion limits children to 100 blocks per create call
        first_batch = children[:100]
        resp = self._client.pages.create(
            parent={"page_id": parent_id},
            properties={"title": [{"text": {"content": title}}]},
            children=first_batch,
        )
        page_id = resp["id"]
        # Append remaining blocks in 100-block chunks
        for i in range(100, len(children), 100):
            self.append_blocks(page_id, children[i:i + 100])
        return page_id

    def update_page_title(self, page_id: str, new_title: str) -> None:
        self._client.pages.update(
            page_id=page_id,
            properties={"title": [{"text": {"content": new_title}}]},
        )

    def get_todo_blocks(self, page_id: str) -> list[dict]:
        """Return [{id, text, checked}] for all to_do blocks in a page."""
        blocks = self.get_all_blocks(page_id)
        todos = []
        for b in blocks:
            if b["type"] == "to_do":
                todos.append({
                    "id": b["id"],
                    "text": _plain_text(b["to_do"]["rich_text"]),
                    "checked": b["to_do"]["checked"],
                })
        return todos

    def delete_block(self, block_id: str) -> None:
        self._client.blocks.delete(block_id=block_id)

    def append_blocks(self, page_id: str, blocks: list[dict]) -> None:
        """Append blocks to a page (max 100 per call — caller must chunk if needed)."""
        if not blocks:
            return
        self._client.blocks.children.append(block_id=page_id, children=blocks)

    def find_callout_block(self, page_id: str, emoji: str) -> dict | None:
        """Find first callout block with matching emoji. Returns {id, text} or None."""
        blocks = self.get_all_blocks(page_id)
        for b in blocks:
            if b["type"] == "callout":
                icon = b["callout"].get("icon", {})
                if icon.get("type") == "emoji" and icon.get("emoji") == emoji:
                    return {
                        "id": b["id"],
                        "text": _plain_text(b["callout"]["rich_text"]),
                    }
        return None

    def update_callout_text(self, block_id: str, new_text: str) -> None:
        self._client.blocks.update(
            block_id=block_id,
            callout={"rich_text": [{"type": "text", "text": {"content": new_text}}]},
        )

    def get_table_rows(self, page_id: str) -> list[dict] | None:
        """Find the first table block in page and return rows as [{id, cells: [str]}].

        Returns None if no table block exists (distinct from empty table → []).
        """
        blocks = self.get_all_blocks(page_id)
        table_block = next((b for b in blocks if b["type"] == "table"), None)
        if table_block is None:
            return None
        rows = _paginate(self._client.blocks.children.list, block_id=table_block["id"])
        result = []
        for row in rows:
            if row["type"] == "table_row":
                cells = [_plain_text(cell) for cell in row["table_row"]["cells"]]
                result.append({"id": row["id"], "cells": cells})
        return result

    def update_table_cell(self, row_id: str, col_idx: int, text: str) -> None:
        """Update a single cell in a table row by fetching current row and patching."""
        row = self._client.blocks.retrieve(block_id=row_id)
        # Copy to avoid mutating the SDK's live response object
        cells = list(row["table_row"]["cells"])
        cells[col_idx] = [{"type": "text", "text": {"content": text}}]
        self._client.blocks.update(block_id=row_id, table_row={"cells": cells})

    def create_calendar_db_entry(self, db_id: str, title: str, date: str) -> None:
        """Add a row to the Notion Calendar database. date must be ISO format: YYYY-MM-DD."""
        self._client.pages.create(
            parent={"database_id": db_id},
            properties={
                "Event": {"title": [{"text": {"content": title}}]},
                "Date": {"date": {"start": date}},
                "Type": {"select": {"name": "Deadline"}},
            },
        )
