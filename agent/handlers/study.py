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
