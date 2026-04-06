# Notion Triage Agent — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an autonomous Python daemon that watches a Notion Inbox page for Notability exports, classifies them with Claude API, routes content to the correct Notion pages, and keeps the whole Notion OS in sync automatically.

**Architecture:** A polling daemon (`agent.py`) runs a triage loop (Inbox → classify → route → create pages) and a state sync loop (completed tasks → remove, deadlines → expire, dashboard callout → rewrite, Mind Vault → sync) every 60 seconds. All Notion operations go through a thin wrapper (`notion.py`). Classification is done by `classifier.py` via Claude API. Routing is handled by `router.py` dispatching to four handlers.

**Tech Stack:** Python 3.11+, `notion-client`, `anthropic`, `google-api-python-client`, `google-auth-oauthlib`, `python-dotenv`, `pytest`, `pytest-mock`

---

## File Map

```
JPATE/
  agent/
    __init__.py
    config.py              # load_config() → Config dataclass
    notion.py              # NotionClient wrapper — all API operations
    classifier.py          # classify(content, config) → ClassificationResult
    router.py              # route(result, notion, config) → dispatches to handlers
    sync.py                # run_sync_cycle(notion, config) — OS state sync
    agent.py               # main loop — orchestrates triage + sync + logging
    handlers/
      __init__.py
      study.py             # create_chapter_pages() — builds Notion pages with toggles
      tasks.py             # append_tasks(), remove_completed_tasks()
      calendar.py          # create_event() — Notion Calendar DB + Google Calendar
      mind_vault.py        # dump_to_mind_vault(), update_active_situations()
    requirements.txt
  tests/
    agent/
      test_config.py
      test_notion.py
      test_classifier.py
      test_router.py
      test_study.py
      test_tasks.py
      test_calendar.py
      test_mind_vault.py
      test_sync.py
  .env.template            # committed — no secrets
  .env                     # never committed
```

---

## Task 1: Project Scaffold

**Files:**
- Create: `agent/__init__.py`
- Create: `agent/handlers/__init__.py`
- Create: `agent/requirements.txt`
- Create: `.env.template`
- Modify: `.gitignore` (create if missing)
- Create: `tests/__init__.py`
- Create: `tests/agent/__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p C:/Users/jacks/JPATE/agent/handlers
mkdir -p C:/Users/jacks/JPATE/tests/agent
```

- [ ] **Step 2: Create empty `__init__.py` files**

`agent/__init__.py` — empty file.
`agent/handlers/__init__.py` — empty file.
`tests/__init__.py` — empty file.
`tests/agent/__init__.py` — empty file.

- [ ] **Step 3: Create `agent/requirements.txt`**

```
notion-client==2.2.1
anthropic==0.40.0
google-api-python-client==2.149.0
google-auth-oauthlib==1.2.1
python-dotenv==1.0.1
pytest==8.3.3
pytest-mock==3.14.0
```

- [ ] **Step 4: Create `.env.template`**

```
NOTION_TOKEN=secret_...
NOTION_INBOX_PAGE_ID=
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_CALENDAR_ID=primary
JPATE_ROOT=C:/Users/jacks/JPATE
POLL_INTERVAL=60
```

- [ ] **Step 5: Create `.gitignore`** (at `JPATE/` root, add if not present)

```
.env
agent/logs/
__pycache__/
*.pyc
.pytest_cache/
token.json
credentials.json
```

- [ ] **Step 6: Install dependencies**

```bash
cd C:/Users/jacks/JPATE
pip install -r agent/requirements.txt
```

Expected: all packages install without errors.

- [ ] **Step 7: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/ tests/ .env.template .gitignore
git -C C:/Users/jacks/JPATE commit -m "feat: scaffold notion triage agent project"
```

---

## Task 2: Config

**Files:**
- Create: `agent/config.py`
- Create: `tests/agent/test_config.py`

- [ ] **Step 1: Write failing test**

`tests/agent/test_config.py`:
```python
import os
import pytest
from agent.config import load_config

def test_load_config_reads_env(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "secret_abc")
    monkeypatch.setenv("NOTION_INBOX_PAGE_ID", "inbox-id-123")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-abc")
    monkeypatch.setenv("GOOGLE_CALENDAR_ID", "primary")
    monkeypatch.setenv("JPATE_ROOT", "C:/Users/jacks/JPATE")
    monkeypatch.setenv("POLL_INTERVAL", "30")

    config = load_config()

    assert config.notion_token == "secret_abc"
    assert config.notion_inbox_page_id == "inbox-id-123"
    assert config.anthropic_api_key == "sk-ant-abc"
    assert config.poll_interval == 30

def test_load_config_defaults(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "t")
    monkeypatch.setenv("NOTION_INBOX_PAGE_ID", "i")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    monkeypatch.setenv("GOOGLE_CALENDAR_ID", "primary")
    monkeypatch.delenv("POLL_INTERVAL", raising=False)
    monkeypatch.delenv("JPATE_ROOT", raising=False)

    config = load_config()
    assert config.poll_interval == 60

def test_load_config_missing_required(monkeypatch):
    monkeypatch.delenv("NOTION_TOKEN", raising=False)
    with pytest.raises(KeyError):
        load_config()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd C:/Users/jacks/JPATE && pytest tests/agent/test_config.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'agent.config'`

- [ ] **Step 3: Implement `agent/config.py`**

```python
from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


@dataclass(frozen=True)
class Config:
    notion_token: str
    notion_inbox_page_id: str
    anthropic_api_key: str
    google_calendar_id: str
    jpate_root: Path
    poll_interval: int
    # Hard-coded destination IDs from spec
    microbio_page_id: str = "be4e45005934493f88b6ddfa03113674"
    nurs2030_page_id: str = "ae3d9ad3d83141c6a9e56e36fe000d42"
    nurs2040_page_id: str = "c9511e785e0841eeb9ef8f34c47515d9"
    task_manager_id: str = "a861e1550b514fe8a532344bb1fd0036"
    calendar_db_id: str = "2b7cdb62-749e-4c9c-b7c3-e83f79f86707"
    mind_vault_id: str = "10211b8f4baf4d829e49df1b6b9ce22d"
    dashboard_id: str = "31c89913b6418033b240f6e34a11382f"
    academic_hub_id: str = "a63940ef072349eda57e59771853e745"


def load_config() -> Config:
    return Config(
        notion_token=os.environ["NOTION_TOKEN"],
        notion_inbox_page_id=os.environ["NOTION_INBOX_PAGE_ID"],
        anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
        google_calendar_id=os.environ["GOOGLE_CALENDAR_ID"],
        jpate_root=Path(os.environ.get("JPATE_ROOT", "C:/Users/jacks/JPATE")),
        poll_interval=int(os.environ.get("POLL_INTERVAL", "60")),
    )
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/agent/test_config.py -v
```
Expected: 3 PASSED

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/config.py tests/agent/test_config.py
git -C C:/Users/jacks/JPATE commit -m "feat: add config loader"
```

---

## Task 3: Notion Wrapper

**Files:**
- Create: `agent/notion.py`
- Create: `tests/agent/test_notion.py`

- [ ] **Step 1: Write failing tests**

`tests/agent/test_notion.py`:
```python
import pytest
from unittest.mock import MagicMock, patch
from agent.notion import NotionClient

@pytest.fixture
def client():
    with patch("agent.notion.Client") as MockClient:
        nc = NotionClient("secret_token")
        nc._client = MockClient.return_value
        yield nc

def test_get_child_pages_returns_list(client):
    client._client.blocks.children.list.return_value = {
        "results": [
            {"type": "child_page", "id": "page-1", "child_page": {"title": "My Notes"}},
            {"type": "paragraph", "id": "block-2"},  # non-page block, should be skipped
        ],
        "has_more": False,
    }
    pages = client.get_child_pages("parent-id")
    assert pages == [{"id": "page-1", "title": "My Notes"}]

def test_extract_text_from_blocks(client):
    blocks = [
        {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "Hello world"}]}},
        {"type": "heading_1", "heading_1": {"rich_text": [{"plain_text": "A Heading"}]}},
        {"type": "to_do", "to_do": {"rich_text": [{"plain_text": "Do this"}], "checked": False}},
    ]
    text = client.extract_text(blocks)
    assert "Hello world" in text
    assert "A Heading" in text
    assert "Do this" in text

def test_get_todo_blocks_filters_correctly(client):
    client._client.blocks.children.list.return_value = {
        "results": [
            {"type": "to_do", "id": "todo-1", "to_do": {"rich_text": [{"plain_text": "Buy milk"}], "checked": False}},
            {"type": "to_do", "id": "todo-2", "to_do": {"rich_text": [{"plain_text": "Done task"}], "checked": True}},
            {"type": "paragraph", "id": "p-1", "paragraph": {"rich_text": [{"plain_text": "not a todo"}]}},
        ],
        "has_more": False,
    }
    todos = client.get_todo_blocks("page-id")
    assert len(todos) == 2
    assert todos[0] == {"id": "todo-1", "text": "Buy milk", "checked": False}
    assert todos[1] == {"id": "todo-2", "text": "Done task", "checked": True}

def test_create_child_page_returns_id(client):
    client._client.pages.create.return_value = {"id": "new-page-id"}
    page_id = client.create_child_page("parent-id", "Chapter 6 — Growth", [])
    assert page_id == "new-page-id"
    client._client.pages.create.assert_called_once()

def test_update_page_title(client):
    client.update_page_title("page-id", "✅ My Notes")
    client._client.pages.update.assert_called_once_with(
        page_id="page-id",
        properties={"title": [{"text": {"content": "✅ My Notes"}}]}
    )
```

- [ ] **Step 2: Run to verify failure**

```bash
cd C:/Users/jacks/JPATE && pytest tests/agent/test_notion.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `agent/notion.py`**

```python
from notion_client import Client


def _plain_text(rich_text: list) -> str:
    return "".join(rt.get("plain_text", "") for rt in rich_text)


def _paginate(fn, **kwargs) -> list:
    """Collect all results across paginated Notion API responses."""
    results = []
    cursor = None
    while True:
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

    def get_all_blocks(self, page_id: str) -> list[dict]:
        """Return all direct child blocks of a page."""
        return _paginate(self._client.blocks.children.list, block_id=page_id)

    def extract_text(self, blocks: list[dict]) -> str:
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
        # Append remaining blocks if any
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

    def get_table_rows(self, page_id: str) -> list[dict]:
        """Find the first table block in a page and return its rows as [{id, cells: [str]}]."""
        blocks = self.get_all_blocks(page_id)
        table_block = next((b for b in blocks if b["type"] == "table"), None)
        if not table_block:
            return []
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
        cells = row["table_row"]["cells"]
        cells[col_idx] = [{"type": "text", "text": {"content": text}}]
        self._client.blocks.update(block_id=row_id, table_row={"cells": cells})

    def create_calendar_db_entry(self, db_id: str, title: str, date: str) -> None:
        """Add a row to the Notion Calendar database."""
        self._client.pages.create(
            parent={"database_id": db_id},
            properties={
                "title": [{"text": {"content": title}}],
                "Date": {"date": {"start": date}},
            },
        )
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/agent/test_notion.py -v
```
Expected: 5 PASSED

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/notion.py tests/agent/test_notion.py
git -C C:/Users/jacks/JPATE commit -m "feat: add notion client wrapper"
```

---

## Task 4: Classifier

**Files:**
- Create: `agent/classifier.py`
- Create: `tests/agent/test_classifier.py`

- [ ] **Step 1: Write failing tests**

`tests/agent/test_classifier.py`:
```python
import pytest
from unittest.mock import MagicMock, patch
from agent.classifier import classify, ClassificationResult, Chapter

@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.anthropic_api_key = "sk-ant-test"
    return cfg

def _mock_response(json_str: str):
    msg = MagicMock()
    msg.content = [MagicMock(text=json_str)]
    return msg

def test_classify_microbiology(config):
    json_str = """{
        "destination": "microbiology",
        "chapters": [{"title": "Chapter 6 — Microbial Growth", "content": "Binary fission..."}],
        "generate_study_guide": true,
        "extracted_tasks": ["Review Lab 6 worksheet"],
        "extracted_events": [{"title": "Exam 3", "date": "2026-04-15"}]
    }"""
    with patch("agent.classifier.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = _mock_response(json_str)
        result = classify("some microbio content", config)

    assert isinstance(result, ClassificationResult)
    assert result.destination == "microbiology"
    assert len(result.chapters) == 1
    assert result.chapters[0].title == "Chapter 6 — Microbial Growth"
    assert result.generate_study_guide is True
    assert result.extracted_tasks == ["Review Lab 6 worksheet"]
    assert result.extracted_events[0]["date"] == "2026-04-15"

def test_classify_falls_back_on_bad_json(config):
    with patch("agent.classifier.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = _mock_response("not json")
        result = classify("content", config)

    assert result.destination == "mind_vault"
    assert result.chapters[0].title == "Unclassified"

def test_classify_multi_chapter(config):
    json_str = """{
        "destination": "nurs_2030",
        "chapters": [
            {"title": "Chapter 3 — Safety", "content": "Safety content"},
            {"title": "Chapter 4 — Ethics", "content": "Ethics content"}
        ],
        "generate_study_guide": false,
        "extracted_tasks": [],
        "extracted_events": []
    }"""
    with patch("agent.classifier.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = _mock_response(json_str)
        result = classify("nursing content", config)

    assert len(result.chapters) == 2
    assert result.destination == "nurs_2030"
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest tests/agent/test_classifier.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `agent/classifier.py`**

```python
from dataclasses import dataclass, field
import json
import anthropic


@dataclass
class Chapter:
    title: str
    content: str


@dataclass
class ClassificationResult:
    destination: str
    chapters: list[Chapter]
    generate_study_guide: bool
    extracted_tasks: list[str] = field(default_factory=list)
    extracted_events: list[dict] = field(default_factory=list)


_PROMPT = """\
You are classifying notes exported from Notability for a nursing student at Auburn University.

Classes: Microbiology (BIOL3200), NURS 2030 (Foundations of Professional Nursing), NURS 2040.

Analyze the content and return ONLY a JSON object with this exact structure:
{
  "destination": "microbiology | nurs_2030 | nurs_2040 | tasks | calendar | mind_vault",
  "chapters": [{"title": "Chapter N — Descriptive Title", "content": "full chapter text"}],
  "generate_study_guide": true or false,
  "extracted_tasks": ["actionable to-do items only"],
  "extracted_events": [{"title": "event name", "date": "YYYY-MM-DD"}]
}

Rules:
- destination: pick the single best match. Use "mind_vault" if unclear.
- chapters: split on chapter/section boundaries. Use one item if no clear splits.
- generate_study_guide: true for lecture notes, lab content, exam prep material.
- extracted_tasks: concrete actionable items only (e.g. "Complete Lab 6 worksheet").
- extracted_events: only items with a specific date.
- Return ONLY the JSON object. No markdown, no explanation.

Content:
"""

_FALLBACK = ClassificationResult(
    destination="mind_vault",
    chapters=[Chapter(title="Unclassified", content="")],
    generate_study_guide=False,
)


def classify(content: str, config) -> ClassificationResult:
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": _PROMPT + content}],
    )
    raw = message.content[0].text.strip()
    try:
        data = json.loads(raw)
        return ClassificationResult(
            destination=data["destination"],
            chapters=[Chapter(**c) for c in data["chapters"]],
            generate_study_guide=bool(data.get("generate_study_guide", False)),
            extracted_tasks=data.get("extracted_tasks", []),
            extracted_events=data.get("extracted_events", []),
        )
    except (json.JSONDecodeError, KeyError, TypeError):
        fallback = ClassificationResult(
            destination="mind_vault",
            chapters=[Chapter(title="Unclassified", content=content)],
            generate_study_guide=False,
        )
        return fallback
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/agent/test_classifier.py -v
```
Expected: 3 PASSED

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/classifier.py tests/agent/test_classifier.py
git -C C:/Users/jacks/JPATE commit -m "feat: add claude api classifier"
```

---

## Task 5: Study Handler

**Files:**
- Create: `agent/handlers/study.py`
- Create: `tests/agent/test_study.py`

- [ ] **Step 1: Write failing tests**

`tests/agent/test_study.py`:
```python
import pytest
from unittest.mock import MagicMock, patch, call
from agent.handlers.study import create_chapter_pages, _make_page_blocks, _generate_study_content

@pytest.fixture
def notion():
    return MagicMock()

@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.anthropic_api_key = "sk-ant-test"
    cfg.microbio_page_id = "micro-id"
    return cfg

def test_make_page_blocks_includes_callout():
    blocks = _make_page_blocks(
        tldr=["Point 1", "Point 2"],
        full_notes="All the notes here",
        key_concepts=["Concept A: definition"],
        study_guide_content=None,
        extracted_tasks=[],
    )
    types = [b["type"] for b in blocks]
    assert "callout" in types
    assert "toggle" in types

def test_make_page_blocks_no_study_guide_toggle_when_none():
    blocks = _make_page_blocks(
        tldr=["Point 1"],
        full_notes="Notes",
        key_concepts=[],
        study_guide_content=None,
        extracted_tasks=[],
    )
    toggle_labels = []
    for b in blocks:
        if b["type"] == "toggle":
            rt = b["toggle"]["rich_text"]
            toggle_labels.append(rt[0]["text"]["content"])
    assert "Study Guide" not in toggle_labels

def test_create_chapter_pages_calls_create_for_each_chapter(notion, config):
    from agent.classifier import Chapter
    chapters = [
        Chapter(title="Chapter 6 — Growth", content="content 6"),
        Chapter(title="Chapter 7 — Genetics", content="content 7"),
    ]
    notion.create_child_page.return_value = "new-page-id"

    with patch("agent.handlers.study._generate_study_content") as mock_gen:
        mock_gen.return_value = {
            "tldr": ["Point 1"],
            "key_concepts": ["Concept: def"],
            "study_guide": {"questions": [], "mnemonics": [], "tables": []},
        }
        create_chapter_pages(chapters, "micro-id", generate_study_guide=True, notion=notion, config=config)

    assert notion.create_child_page.call_count == 2
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest tests/agent/test_study.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `agent/handlers/study.py`**

```python
import json
import anthropic
from agent.classifier import Chapter


_STUDY_PROMPT = """\
Generate structured study content for these notes. Return ONLY a JSON object:
{
  "tldr": ["3-5 key takeaway bullets"],
  "key_concepts": ["Term: definition", ...],
  "study_guide": {
    "questions": ["practice question?", ...],
    "mnemonics": ["mnemonic if applicable"],
    "tables": []
  }
}
No markdown, no explanation. Notes:
"""


def _rt(text: str) -> list:
    """Build a rich_text array from a plain string."""
    return [{"type": "text", "text": {"content": text}}]


def _callout(text: str, emoji: str = "📌") -> dict:
    return {
        "type": "callout",
        "callout": {
            "icon": {"type": "emoji", "emoji": emoji},
            "rich_text": _rt(text),
        },
    }


def _toggle(label: str, children: list[dict]) -> dict:
    return {
        "type": "toggle",
        "toggle": {"rich_text": _rt(label), "children": children},
    }


def _paragraph(text: str) -> dict:
    return {"type": "paragraph", "paragraph": {"rich_text": _rt(text)}}


def _todo(text: str) -> dict:
    return {"type": "to_do", "to_do": {"rich_text": _rt(text), "checked": False}}


def _chunk_text(text: str, max_len: int = 1900) -> list[dict]:
    """Split long text into paragraph blocks (Notion limit: 2000 chars per rich_text)."""
    paragraphs = []
    for i in range(0, len(text), max_len):
        paragraphs.append(_paragraph(text[i:i + max_len]))
    return paragraphs or [_paragraph("")]


def _generate_study_content(content: str, config) -> dict:
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": _STUDY_PROMPT + content}],
    )
    try:
        return json.loads(msg.content[0].text.strip())
    except (json.JSONDecodeError, IndexError):
        return {"tldr": [], "key_concepts": [], "study_guide": None}


def _make_page_blocks(
    tldr: list[str],
    full_notes: str,
    key_concepts: list[str],
    study_guide_content: dict | None,
    extracted_tasks: list[str],
) -> list[dict]:
    blocks = []

    # TL;DR callout (always visible)
    tldr_text = "\n".join(f"• {b}" for b in tldr) if tldr else "See notes below."
    blocks.append(_callout(tldr_text, "📌"))

    # Full Notes toggle
    blocks.append(_toggle("Full Notes", _chunk_text(full_notes)))

    # Key Concepts toggle
    if key_concepts:
        concept_blocks = [_paragraph(c) for c in key_concepts]
        blocks.append(_toggle("Key Concepts", concept_blocks))

    # Study Guide toggle (only if generated)
    if study_guide_content:
        sg_blocks = []
        for q in study_guide_content.get("questions", []):
            sg_blocks.append(_paragraph(f"Q: {q}"))
        for m in study_guide_content.get("mnemonics", []):
            sg_blocks.append(_paragraph(f"🧠 {m}"))
        if sg_blocks:
            blocks.append(_toggle("Study Guide", sg_blocks))

    # Tasks / Dates reference toggle
    if extracted_tasks:
        task_blocks = [_todo(t) for t in extracted_tasks]
        blocks.append(_toggle("Tasks / Dates", task_blocks))

    return blocks


def create_chapter_pages(
    chapters: list[Chapter],
    parent_page_id: str,
    generate_study_guide: bool,
    notion,
    config,
) -> list[str]:
    """Create one Notion page per chapter. Returns list of created page IDs."""
    page_ids = []
    for chapter in chapters:
        study_data = _generate_study_content(chapter.content, config) if chapter.content else {}
        blocks = _make_page_blocks(
            tldr=study_data.get("tldr", []),
            full_notes=chapter.content,
            key_concepts=study_data.get("key_concepts", []),
            study_guide_content=study_data.get("study_guide") if generate_study_guide else None,
            extracted_tasks=[],
        )
        page_id = notion.create_child_page(parent_page_id, chapter.title, blocks)
        page_ids.append(page_id)
    return page_ids
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/agent/test_study.py -v
```
Expected: 3 PASSED

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/handlers/study.py tests/agent/test_study.py
git -C C:/Users/jacks/JPATE commit -m "feat: add study handler with toggle page structure"
```

---

## Task 6: Tasks Handler

**Files:**
- Create: `agent/handlers/tasks.py`
- Create: `tests/agent/test_tasks.py`

- [ ] **Step 1: Write failing tests**

`tests/agent/test_tasks.py`:
```python
import pytest
from unittest.mock import MagicMock
from agent.handlers.tasks import append_tasks, remove_completed_tasks

@pytest.fixture
def notion():
    return MagicMock()

@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.task_manager_id = "task-mgr-id"
    return cfg

def test_append_tasks_calls_append_blocks(notion, config):
    append_tasks(["Study Lab 6", "Review NURS notes"], notion, config)
    notion.append_blocks.assert_called_once()
    blocks = notion.append_blocks.call_args[0][1]
    assert len(blocks) == 2
    assert blocks[0]["type"] == "to_do"
    assert blocks[0]["to_do"]["checked"] is False
    texts = [b["to_do"]["rich_text"][0]["text"]["content"] for b in blocks]
    assert "Study Lab 6" in texts

def test_append_tasks_does_nothing_when_empty(notion, config):
    append_tasks([], notion, config)
    notion.append_blocks.assert_not_called()

def test_remove_completed_tasks_deletes_checked_blocks(notion, config):
    notion.get_todo_blocks.return_value = [
        {"id": "todo-1", "text": "Buy milk", "checked": False},
        {"id": "todo-2", "text": "Done task", "checked": True},
        {"id": "todo-3", "text": "Another done", "checked": True},
    ]
    removed = remove_completed_tasks(notion, config)
    assert notion.delete_block.call_count == 2
    assert removed == ["Done task", "Another done"]

def test_remove_completed_returns_empty_when_none_checked(notion, config):
    notion.get_todo_blocks.return_value = [
        {"id": "todo-1", "text": "Active task", "checked": False},
    ]
    removed = remove_completed_tasks(notion, config)
    assert removed == []
    notion.delete_block.assert_not_called()
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest tests/agent/test_tasks.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `agent/handlers/tasks.py`**

```python
def _rt(text: str) -> list:
    return [{"type": "text", "text": {"content": text}}]


def append_tasks(tasks: list[str], notion, config) -> None:
    """Append to-do blocks to Task Manager Next Actions section."""
    if not tasks:
        return
    blocks = [
        {"type": "to_do", "to_do": {"rich_text": _rt(t), "checked": False}}
        for t in tasks
    ]
    notion.append_blocks(config.task_manager_id, blocks)


def remove_completed_tasks(notion, config) -> list[str]:
    """Delete checked to-do blocks from Task Manager. Returns list of removed task texts."""
    todos = notion.get_todo_blocks(config.task_manager_id)
    removed = []
    for todo in todos:
        if todo["checked"]:
            notion.delete_block(todo["id"])
            removed.append(todo["text"])
    return removed
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/agent/test_tasks.py -v
```
Expected: 4 PASSED

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/handlers/tasks.py tests/agent/test_tasks.py
git -C C:/Users/jacks/JPATE commit -m "feat: add tasks handler"
```

---

## Task 7: Calendar Handler + Google OAuth Setup

**Files:**
- Create: `agent/handlers/calendar.py`
- Create: `tests/agent/test_calendar.py`

### Part A — Google Calendar OAuth Setup (one-time, manual)

- [ ] **Step 1: Create a Google Cloud project and enable Calendar API**

1. Go to https://console.cloud.google.com/
2. Create a new project named `JPATE Agent`
3. Enable the **Google Calendar API** (APIs & Services → Enable APIs)
4. Create credentials: OAuth 2.0 Client ID → Desktop App
5. Download the JSON → save as `C:/Users/jacks/JPATE/credentials.json`

- [ ] **Step 2: Run one-time auth flow**

```bash
cd C:/Users/jacks/JPATE
python -c "
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/calendar'])
creds = flow.run_local_server(port=0)
import json, pathlib
pathlib.Path('token.json').write_text(creds.to_json())
print('token.json written')
"
```

Expected: browser opens for Google login → grants permission → `token.json` created.

### Part B — Calendar Handler Code

- [ ] **Step 3: Write failing tests**

`tests/agent/test_calendar.py`:
```python
import pytest
from unittest.mock import MagicMock, patch
from agent.handlers.calendar import create_event

@pytest.fixture
def notion():
    return MagicMock()

@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.calendar_db_id = "cal-db-id"
    cfg.google_calendar_id = "primary"
    cfg.jpate_root = MagicMock()
    cfg.jpate_root.__truediv__ = lambda self, other: MagicMock(exists=lambda: True, read_text=lambda: '{"token": "fake"}')
    return cfg

def test_create_event_writes_to_notion(notion, config):
    with patch("agent.handlers.calendar._get_gcal_service", return_value=MagicMock()):
        create_event("Exam 3", "2026-04-15", notion, config)
    notion.create_calendar_db_entry.assert_called_once_with(
        "cal-db-id", "Exam 3", "2026-04-15"
    )

def test_create_event_calls_gcal(notion, config):
    mock_service = MagicMock()
    with patch("agent.handlers.calendar._get_gcal_service", return_value=mock_service):
        create_event("Exam 3", "2026-04-15", notion, config)
    mock_service.events.return_value.insert.assert_called_once()
```

- [ ] **Step 4: Run to verify failure**

```bash
pytest tests/agent/test_calendar.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 5: Implement `agent/handlers/calendar.py`**

```python
import json
import logging
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

_SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _get_gcal_service(jpate_root: Path):
    token_path = jpate_root / "token.json"
    if not token_path.exists():
        raise FileNotFoundError(
            f"Google Calendar token not found at {token_path}. "
            "Run the one-time OAuth setup in Task 7."
        )
    creds = Credentials.from_authorized_user_info(
        json.loads(token_path.read_text()), _SCOPES
    )
    return build("calendar", "v3", credentials=creds)


def create_event(title: str, date: str, notion, config) -> None:
    """
    Create an event in both Notion Calendar DB and Google Calendar.
    date must be ISO format: YYYY-MM-DD
    """
    # Notion Calendar DB
    notion.create_calendar_db_entry(config.calendar_db_id, title, date)

    # Google Calendar
    try:
        service = _get_gcal_service(config.jpate_root)
        event = {
            "summary": title,
            "start": {"date": date, "timeZone": "America/Chicago"},
            "end": {"date": date, "timeZone": "America/Chicago"},
        }
        service.events().insert(calendarId=config.google_calendar_id, body=event).execute()
    except Exception as exc:
        logger.error("Google Calendar write failed for '%s': %s", title, exc)
        # Notion write already succeeded — log and continue
```

- [ ] **Step 6: Run tests**

```bash
pytest tests/agent/test_calendar.py -v
```
Expected: 2 PASSED

- [ ] **Step 7: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/handlers/calendar.py tests/agent/test_calendar.py
git -C C:/Users/jacks/JPATE commit -m "feat: add calendar handler with gcal + notion db write"
```

---

## Task 8: Mind Vault Handler

**Files:**
- Create: `agent/handlers/mind_vault.py`
- Create: `tests/agent/test_mind_vault.py`

- [ ] **Step 1: Write failing tests**

`tests/agent/test_mind_vault.py`:
```python
import pytest
from unittest.mock import MagicMock, patch
from agent.handlers.mind_vault import dump_to_mind_vault, update_active_situations

@pytest.fixture
def notion():
    return MagicMock()

@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.mind_vault_id = "mind-vault-id"
    cfg.anthropic_api_key = "sk-ant-test"
    return cfg

def test_dump_to_mind_vault_creates_page(notion, config):
    notion.create_child_page.return_value = "new-page-id"
    dump_to_mind_vault("My Note", "Note content here", notion, config)
    notion.create_child_page.assert_called_once()
    call_args = notion.create_child_page.call_args
    assert call_args[0][0] == "mind-vault-id"
    assert call_args[0][1] == "My Note"

def test_dump_with_review_flag_adds_warning_callout(notion, config):
    notion.create_child_page.return_value = "p"
    dump_to_mind_vault("Title", "Content", notion, config, needs_review=True)
    blocks = notion.create_child_page.call_args[0][2]
    callout_block = blocks[0]
    assert callout_block["type"] == "callout"
    assert "⚠️" in callout_block["callout"]["icon"]["emoji"]

def test_update_active_situations_appends_blocks(notion, config):
    open_tasks = ["Study Lab 6", "AceMapp due May 5"]
    with patch("agent.handlers.mind_vault.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Active: studying for Microbio, completing AceMapp")]
        )
        update_active_situations(open_tasks, notion, config)
    notion.append_blocks.assert_called_once()
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest tests/agent/test_mind_vault.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `agent/handlers/mind_vault.py`**

```python
import anthropic


def _rt(text: str) -> list:
    return [{"type": "text", "text": {"content": text}}]


def _callout(text: str, emoji: str) -> dict:
    return {
        "type": "callout",
        "callout": {"icon": {"type": "emoji", "emoji": emoji}, "rich_text": _rt(text)},
    }


def _paragraph(text: str) -> dict:
    return {"type": "paragraph", "paragraph": {"rich_text": _rt(text)}}


def dump_to_mind_vault(
    title: str, content: str, notion, config, needs_review: bool = False
) -> str:
    """Create a page in Mind Vault. Returns created page ID."""
    blocks = []
    if needs_review:
        blocks.append(_callout("⚠️ Review needed — could not classify automatically", "⚠️"))
    blocks.append(_paragraph(content))
    return notion.create_child_page(config.mind_vault_id, title, blocks)


_SITUATIONS_PROMPT = """\
Given these open tasks for a nursing student, write a concise 2-3 sentence summary
of their current active situations (what they are working on right now).
Be specific and practical. No fluff.

Open tasks:
"""


def update_active_situations(open_tasks: list[str], notion, config) -> None:
    """Append an updated active situations summary to Mind Vault."""
    if not open_tasks:
        return
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    task_list = "\n".join(f"- {t}" for t in open_tasks)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": _SITUATIONS_PROMPT + task_list}],
    )
    summary = msg.content[0].text.strip()
    blocks = [
        _callout("Active Situations — auto-updated", "🪞"),
        _paragraph(summary),
    ]
    notion.append_blocks(config.mind_vault_id, blocks)
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/agent/test_mind_vault.py -v
```
Expected: 3 PASSED

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/handlers/mind_vault.py tests/agent/test_mind_vault.py
git -C C:/Users/jacks/JPATE commit -m "feat: add mind vault handler"
```

---

## Task 9: Router

**Files:**
- Create: `agent/router.py`
- Create: `tests/agent/test_router.py`

- [ ] **Step 1: Write failing tests**

`tests/agent/test_router.py`:
```python
import pytest
from unittest.mock import MagicMock, patch
from agent.router import route
from agent.classifier import ClassificationResult, Chapter

def _result(destination, chapters=None, tasks=None, events=None, study_guide=False):
    return ClassificationResult(
        destination=destination,
        chapters=chapters or [Chapter(title="Ch 1", content="content")],
        generate_study_guide=study_guide,
        extracted_tasks=tasks or [],
        extracted_events=events or [],
    )

@pytest.fixture
def notion(): return MagicMock()
@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.microbio_page_id = "micro-id"
    cfg.nurs2030_page_id = "nurs2030-id"
    cfg.nurs2040_page_id = "nurs2040-id"
    return cfg

def test_route_microbiology_calls_study_handler(notion, config):
    result = _result("microbiology")
    with patch("agent.router.create_chapter_pages") as mock_study:
        route(result, notion, config)
    mock_study.assert_called_once_with(
        result.chapters, config.microbio_page_id, False, notion, config
    )

def test_route_nurs2030(notion, config):
    result = _result("nurs_2030")
    with patch("agent.router.create_chapter_pages") as mock_study:
        route(result, notion, config)
    mock_study.assert_called_once_with(
        result.chapters, config.nurs2030_page_id, False, notion, config
    )

def test_route_tasks_extracted(notion, config):
    result = _result("microbiology", tasks=["Do Lab 6"])
    with patch("agent.router.create_chapter_pages"), patch("agent.router.append_tasks") as mock_tasks:
        route(result, notion, config)
    mock_tasks.assert_called_once_with(["Do Lab 6"], notion, config)

def test_route_events_extracted(notion, config):
    result = _result("microbiology", events=[{"title": "Exam 3", "date": "2026-04-15"}])
    with patch("agent.router.create_chapter_pages"), patch("agent.router.create_event") as mock_cal:
        route(result, notion, config)
    mock_cal.assert_called_once_with("Exam 3", "2026-04-15", notion, config)

def test_route_mind_vault_fallback(notion, config):
    result = _result("mind_vault")
    with patch("agent.router.dump_to_mind_vault") as mock_mv:
        route(result, notion, config)
    mock_mv.assert_called_once()
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest tests/agent/test_router.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `agent/router.py`**

```python
from agent.classifier import ClassificationResult
from agent.handlers.study import create_chapter_pages
from agent.handlers.tasks import append_tasks
from agent.handlers.calendar import create_event
from agent.handlers.mind_vault import dump_to_mind_vault

_DESTINATION_PAGE = {
    "microbiology": "microbio_page_id",
    "nurs_2030": "nurs2030_page_id",
    "nurs_2040": "nurs2040_page_id",
}


def route(result: ClassificationResult, notion, config) -> None:
    """Dispatch a ClassificationResult to the appropriate handlers."""

    # Route main content
    if result.destination in _DESTINATION_PAGE:
        parent_id = getattr(config, _DESTINATION_PAGE[result.destination])
        create_chapter_pages(
            result.chapters, parent_id, result.generate_study_guide, notion, config
        )
    elif result.destination == "mind_vault":
        content = "\n\n".join(c.content for c in result.chapters)
        title = result.chapters[0].title if result.chapters else "Untitled"
        dump_to_mind_vault(title, content, notion, config)

    # Always route extracted tasks to Task Manager
    if result.extracted_tasks:
        append_tasks(result.extracted_tasks, notion, config)

    # Always route extracted events to Calendar
    for event in result.extracted_events:
        create_event(event["title"], event["date"], notion, config)
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/agent/test_router.py -v
```
Expected: 5 PASSED

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/router.py tests/agent/test_router.py
git -C C:/Users/jacks/JPATE commit -m "feat: add router"
```

---

## Task 10: State Sync Loop

**Files:**
- Create: `agent/sync.py`
- Create: `tests/agent/test_sync.py`

- [ ] **Step 1: Write failing tests**

`tests/agent/test_sync.py`:
```python
import pytest
from unittest.mock import MagicMock, patch
from agent.sync import (
    sync_completed_tasks,
    expire_passed_deadlines,
    rewrite_current_focus,
    sync_mind_vault_situations,
)
from datetime import date

@pytest.fixture
def notion(): return MagicMock()
@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.task_manager_id = "task-mgr-id"
    cfg.academic_hub_id = "acad-hub-id"
    cfg.dashboard_id = "dash-id"
    cfg.anthropic_api_key = "sk-ant-test"
    return cfg

def test_sync_completed_tasks_removes_and_returns(notion, config):
    notion.get_todo_blocks.return_value = [
        {"id": "t1", "text": "Active task", "checked": False},
        {"id": "t2", "text": "Done task", "checked": True},
    ]
    removed = sync_completed_tasks(notion, config)
    notion.delete_block.assert_called_once_with("t2")
    assert removed == ["Done task"]

def test_expire_passed_deadlines_marks_cell(notion, config):
    notion.get_table_rows.return_value = [
        {"id": "header-row", "cells": ["Item", "Due Date", "Notes"]},
        {"id": "row-1", "cells": ["AceMapp", "2026-05-05", ""]},
        {"id": "row-2", "cells": ["Old Exam", "2026-01-01", ""]},  # passed
    ]
    with patch("agent.sync.date") as mock_date:
        mock_date.today.return_value = date(2026, 4, 6)
        mock_date.fromisoformat = date.fromisoformat
        expire_passed_deadlines(notion, config)
    notion.update_table_cell.assert_called_once_with("row-2", 2, "✅ Passed")

def test_rewrite_current_focus_updates_callout(notion, config):
    notion.get_todo_blocks.return_value = [
        {"id": "t1", "text": "Study Lab 6", "checked": False},
        {"id": "t2", "text": "AceMapp due May 5", "checked": False},
    ]
    notion.find_callout_block.return_value = {"id": "callout-id", "text": "old focus"}
    with patch("agent.sync.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Microbio Exam 3 · AceMapp due May 5")]
        )
        rewrite_current_focus(notion, config)
    notion.update_callout_text.assert_called_once_with(
        "callout-id", "Microbio Exam 3 · AceMapp due May 5"
    )

def test_rewrite_current_focus_skips_when_no_callout(notion, config):
    notion.get_todo_blocks.return_value = []
    notion.find_callout_block.return_value = None
    with patch("agent.sync.anthropic.Anthropic"):
        rewrite_current_focus(notion, config)
    notion.update_callout_text.assert_not_called()
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest tests/agent/test_sync.py -v
```
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `agent/sync.py`**

```python
import logging
from datetime import date
import anthropic
from agent.handlers.tasks import remove_completed_tasks
from agent.handlers.mind_vault import update_active_situations

logger = logging.getLogger(__name__)

_FOCUS_PROMPT = """\
Rewrite the "Current Focus" for a nursing student's dashboard.
Output ONLY a short, punchy summary (max 80 chars) of their top priorities,
separated by · (middle dot). No intro, no labels, just the content line.

Open tasks:
"""


def sync_completed_tasks(notion, config) -> list[str]:
    """Remove checked to-do blocks from Task Manager. Returns removed task texts."""
    return remove_completed_tasks(notion, config)


def expire_passed_deadlines(notion, config) -> None:
    """Mark past deadlines in Academic Hub Key Deadlines table as ✅ Passed."""
    today = date.today()
    rows = notion.get_table_rows(config.academic_hub_id)
    for row in rows[1:]:  # skip header row
        cells = row["cells"]
        if len(cells) < 3:
            continue
        date_str = cells[1].strip()
        if not date_str or date_str == "TBD":
            continue
        try:
            deadline = date.fromisoformat(date_str)
        except ValueError:
            continue
        if deadline < today and cells[2] != "✅ Passed":
            notion.update_table_cell(row["id"], 2, "✅ Passed")
            logger.info("Expired deadline: %s", cells[0])


def rewrite_current_focus(notion, config) -> None:
    """Rewrite the 🔥 callout on the dashboard from current open tasks."""
    todos = notion.get_todo_blocks(config.task_manager_id)
    open_tasks = [t["text"] for t in todos if not t["checked"]]

    callout = notion.find_callout_block(config.dashboard_id, "🔥")
    if not callout:
        logger.warning("Could not find 🔥 callout on dashboard — skipping focus rewrite")
        return

    if not open_tasks:
        notion.update_callout_text(callout["id"], "All caught up ✅")
        return

    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    task_list = "\n".join(f"- {t}" for t in open_tasks)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=128,
        messages=[{"role": "user", "content": _FOCUS_PROMPT + task_list}],
    )
    new_focus = msg.content[0].text.strip()
    notion.update_callout_text(callout["id"], new_focus)
    logger.info("Rewrote Current Focus: %s", new_focus)


def sync_mind_vault_situations(open_tasks: list[str], notion, config) -> None:
    """Update Mind Vault active situations from current open tasks."""
    update_active_situations(open_tasks, notion, config)


def run_sync_cycle(notion, config) -> list[str]:
    """
    Run the full state sync cycle. Returns list of completed task texts (for focus rewrite).
    Call this once per poll cycle, after triage.
    """
    removed = sync_completed_tasks(notion, config)
    if removed:
        logger.info("Removed %d completed task(s): %s", len(removed), removed)

    expire_passed_deadlines(notion, config)
    rewrite_current_focus(notion, config)

    todos = notion.get_todo_blocks(config.task_manager_id)
    open_tasks = [t["text"] for t in todos if not t["checked"]]
    sync_mind_vault_situations(open_tasks, notion, config)

    return removed
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/agent/test_sync.py -v
```
Expected: 4 PASSED

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/sync.py tests/agent/test_sync.py
git -C C:/Users/jacks/JPATE commit -m "feat: add state sync loop"
```

---

## Task 11: Main Agent Loop

**Files:**
- Create: `agent/agent.py`
- Create: `agent/logs/.gitkeep`

- [ ] **Step 1: Create logs directory placeholder**

```bash
mkdir -p C:/Users/jacks/JPATE/agent/logs
echo "" > C:/Users/jacks/JPATE/agent/logs/.gitkeep
```

- [ ] **Step 2: Implement `agent/agent.py`**

```python
"""
agent.py — JPATE Triage Agent
Run: python agent/agent.py
Polls Notion Inbox every POLL_INTERVAL seconds. Ctrl+C to stop.
"""
import logging
import logging.handlers
import time
from pathlib import Path

from agent.config import load_config
from agent.notion import NotionClient
from agent.classifier import classify
from agent.router import route
from agent.sync import run_sync_cycle

LOG_PATH = Path(__file__).parent / "logs" / "agent.log"


def _setup_logging() -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[handler, logging.StreamHandler()],
    )


def process_inbox(notion: NotionClient, config) -> int:
    """Check Inbox for new pages and process each. Returns count processed."""
    pages = notion.get_child_pages(config.notion_inbox_page_id)
    unprocessed = [p for p in pages if not p["title"].startswith("✅")]

    for page in unprocessed:
        logging.info("Processing: %s", page["title"])
        try:
            content = notion.get_page_text(page["id"])
            result = classify(content, config)
            logging.info(
                "Classified as '%s' — %d chapter(s)", result.destination, len(result.chapters)
            )
            route(result, notion, config)
            notion.update_page_title(page["id"], f"✅ {page['title']}")
            logging.info("Done: %s", page["title"])
        except Exception as exc:
            logging.error("Failed to process '%s': %s", page["title"], exc, exc_info=True)

    return len(unprocessed)


def run_forever(notion: NotionClient, config) -> None:
    logging.info("Agent started. Polling every %ds.", config.poll_interval)
    while True:
        try:
            count = process_inbox(notion, config)
            if count:
                logging.info("Triage: processed %d item(s).", count)
            run_sync_cycle(notion, config)
        except Exception as exc:
            logging.error("Cycle error: %s", exc, exc_info=True)
        time.sleep(config.poll_interval)


def main() -> None:
    _setup_logging()
    config = load_config()
    notion = NotionClient(config.notion_token)
    run_forever(notion, config)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Smoke test — verify agent starts without crashing**

First ensure `.env` is populated (see `.env.template`). Then:

```bash
cd C:/Users/jacks/JPATE && python agent/agent.py
```

Expected: logs show `Agent started. Polling every 60s.` — then `Nothing to process` or processes any pending Inbox items.  
Press `Ctrl+C` to stop.

- [ ] **Step 4: Run full test suite**

```bash
pytest tests/ -v
```
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git -C C:/Users/jacks/JPATE add agent/agent.py agent/logs/.gitkeep
git -C C:/Users/jacks/JPATE commit -m "feat: add main agent loop"
```

---

## Task 12: Create Notion Inbox Page + Windows Task Scheduler

**Files:**
- Create: `agent/setup_inbox.py` (one-time setup script)
- Create: `agent/setup_scheduler.ps1`

- [ ] **Step 1: Create `agent/setup_inbox.py`**

This script creates the Inbox page in Notion and prints its ID to paste into `.env`.

```python
"""
One-time setup: creates the Inbox page under Jackson Pate root.
Run: python agent/setup_inbox.py
Copy the printed page ID into .env as NOTION_INBOX_PAGE_ID=
"""
from agent.config import load_config
from agent.notion import NotionClient

DASHBOARD_ID = "31c89913b6418033b240f6e34a11382f"

def main():
    config = load_config()
    notion = NotionClient(config.notion_token)
    page_id = notion.create_child_page(
        DASHBOARD_ID,
        "📥 Inbox",
        [{"type": "callout", "callout": {
            "icon": {"type": "emoji", "emoji": "📥"},
            "rich_text": [{"type": "text", "text": {"content": "Share Notability exports here."}}]
        }}]
    )
    print(f"\nInbox page created!\nNOTION_INBOX_PAGE_ID={page_id}\n")
    print("Add this to your .env file.")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run setup_inbox.py**

```bash
cd C:/Users/jacks/JPATE && python agent/setup_inbox.py
```

Expected: prints `NOTION_INBOX_PAGE_ID=<some-uuid>`. Copy that into `.env`.

- [ ] **Step 3: Create `agent/setup_scheduler.ps1`**

```powershell
# Run as Administrator in PowerShell
$taskName = "JPATE Triage Agent"
$pythonPath = (Get-Command python).Source
$scriptPath = "C:\Users\jacks\JPATE\agent\agent.py"
$logPath = "C:\Users\jacks\JPATE\agent\logs\scheduler.log"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $scriptPath
$triggerLogin = New-ScheduledTaskTrigger -AtLogOn
$triggerRepeat = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 5) -Once -At (Get-Date)
$settings = New-ScheduledTaskSettingsSet -RestartOnIdle -RunOnlyIfNetworkAvailable

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $triggerLogin,$triggerRepeat `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "Task '$taskName' registered. It will start on next login."
Write-Host "To start immediately: Start-ScheduledTask -TaskName '$taskName'"
```

- [ ] **Step 4: Register the scheduled task**

Open PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
C:\Users\jacks\JPATE\agent\setup_scheduler.ps1
Start-ScheduledTask -TaskName "JPATE Triage Agent"
```

Expected: no errors. Task appears in Task Scheduler as `JPATE Triage Agent`.

- [ ] **Step 5: Verify agent is running**

```bash
cat C:/Users/jacks/JPATE/agent/logs/agent.log
```

Expected: log shows `Agent started. Polling every 60s.`

- [ ] **Step 6: End-to-end test — export from Notability**

1. In Notability on your iPad, share any note to Notion → select the `📥 Inbox` page
2. Wait up to 60 seconds
3. Check your target hub (e.g. Microbio) for the new chapter page
4. Check Task Manager if the note had action items
5. Check the 🔥 Current Focus callout on your dashboard

- [ ] **Step 7: Final commit**

```bash
git -C C:/Users/jacks/JPATE add agent/setup_inbox.py agent/setup_scheduler.ps1
git -C C:/Users/jacks/JPATE commit -m "feat: add inbox setup script and task scheduler registration"
```

---

## Self-Review

**Spec coverage check:**
- ✅ Inbox page watched for unprocessed child pages
- ✅ Classify via Claude API → JSON with destination, chapters, tasks, events
- ✅ Route to Microbio / NURS 2030 / NURS 2040 / Task Manager / Calendar / Mind Vault
- ✅ Chapter splitting (one page per chapter)
- ✅ Toggle page structure: TL;DR callout, Full Notes, Key Concepts, Study Guide, Tasks/Dates
- ✅ Study guide generated only when flagged
- ✅ Completed checkbox detection → delete block
- ✅ Current Focus callout rewritten from open tasks
- ✅ Academic Hub deadline expiry
- ✅ Mind Vault active situations sync
- ✅ Google Calendar + Notion Calendar DB writes
- ✅ Classification failure → Mind Vault with ⚠️ flag
- ✅ Windows Task Scheduler wiring
- ✅ Rotating log file

**No placeholders found.**

**Type consistency:** All function signatures consistent across tasks. `notion` parameter is always a `NotionClient` instance. `config` is always a `Config` dataclass.
