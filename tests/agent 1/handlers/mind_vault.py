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


def _paragraphs(text: str, chunk_size: int = 1900) -> list[dict]:
    """Split text into paragraph blocks respecting Notion's 2000-char limit."""
    return [_paragraph(text[i:i + chunk_size]) for i in range(0, max(len(text), 1), chunk_size)]


def dump_to_mind_vault(
    title: str, content: str, notion, config, needs_review: bool = False
) -> str:
    """Create a page in Mind Vault. Returns created page ID."""
    blocks = []
    if needs_review:
        blocks.append(_callout("⚠️ Review needed — could not classify automatically", "⚠️"))
    blocks.extend(_paragraphs(content))
    return notion.create_child_page(config.mind_vault_id, title, blocks)


_SITUATIONS_PROMPT = """\
Given these open tasks for a nursing student, write a concise 2-3 sentence summary
of their current active situations (what they are working on right now).
Be specific and practical. No fluff.

Open tasks:
"""


def update_active_situations(open_tasks: list[str], notion, config) -> None:
    """Update the 🪞 Active Situations callout in Mind Vault, creating it if absent."""
    if not open_tasks:
        return
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    task_list = "\n".join(f"- {t}" for t in open_tasks)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": _SITUATIONS_PROMPT + task_list}],
    )
    if not msg.content:
        return
    summary = msg.content[0].text.strip()
    existing = notion.find_callout_block(config.mind_vault_id, "🪞")
    if existing:
        notion.update_callout_text(existing["id"], summary)
    else:
        notion.append_blocks(config.mind_vault_id, [_callout(summary, "🪞")])
