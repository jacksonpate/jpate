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
    if not rows:
        return
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


def rewrite_current_focus(notion, config, open_tasks: list[str] | None = None) -> None:
    """Rewrite the 🔥 callout on the dashboard from current open tasks.

    Accepts pre-fetched open_tasks to avoid a redundant get_todo_blocks call
    when called from run_sync_cycle.
    """
    if open_tasks is None:
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
    if not msg.content:
        logger.warning("Claude returned empty content for focus rewrite — skipping")
        return
    new_focus = msg.content[0].text.strip()
    notion.update_callout_text(callout["id"], new_focus)
    logger.info("Rewrote Current Focus: %s", new_focus)


def sync_mind_vault_situations(open_tasks: list[str], notion, config) -> None:
    """Update Mind Vault active situations from current open tasks."""
    update_active_situations(open_tasks, notion, config)


def run_sync_cycle(notion, config) -> list[str]:
    """
    Run the full state sync cycle. Returns list of completed task texts.
    Call once per poll cycle, after triage.
    """
    removed = sync_completed_tasks(notion, config)
    if removed:
        logger.info("Removed %d completed task(s): %s", len(removed), removed)

    expire_passed_deadlines(notion, config)

    todos = notion.get_todo_blocks(config.task_manager_id)
    open_tasks = [t["text"] for t in todos if not t["checked"]]
    rewrite_current_focus(notion, config, open_tasks=open_tasks)
    sync_mind_vault_situations(open_tasks, notion, config)

    return removed
