import difflib


def _rt(text: str) -> list:
    return [{"type": "text", "text": {"content": text}}]


def _is_duplicate(task: str, existing: list[str], threshold: float = 0.82) -> bool:
    """Return True if task is similar enough to any existing task."""
    t = task.strip().lower()
    for e in existing:
        ratio = difflib.SequenceMatcher(None, t, e).ratio()
        if ratio >= threshold:
            return True
    return False


def append_tasks(tasks: list[str], notion, config) -> None:
    """Append to-do blocks to Task Manager, skipping near-duplicates."""
    if not tasks:
        return
    existing = [t["text"].strip().lower() for t in notion.get_todo_blocks(config.task_manager_id)]
    new_tasks = []
    for t in tasks:
        if not _is_duplicate(t, existing + [x.strip().lower() for x in new_tasks]):
            new_tasks.append(t)
    if not new_tasks:
        return
    blocks = [
        {"type": "to_do", "to_do": {"rich_text": _rt(t), "checked": False}}
        for t in new_tasks
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
