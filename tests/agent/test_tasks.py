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
