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
