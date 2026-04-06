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
