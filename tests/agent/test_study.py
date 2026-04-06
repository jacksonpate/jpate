import pytest
from unittest.mock import MagicMock, patch
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
