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
