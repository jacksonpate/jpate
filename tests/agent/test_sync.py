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
