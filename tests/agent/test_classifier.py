import pytest
from unittest.mock import MagicMock, patch
from agent.classifier import classify, ClassificationResult, Chapter

@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.anthropic_api_key = "sk-ant-test"
    return cfg

def _mock_response(json_str: str):
    msg = MagicMock()
    msg.content = [MagicMock(text=json_str)]
    return msg

def test_classify_microbiology(config):
    json_str = """{
        "destination": "microbiology",
        "chapters": [{"title": "Chapter 6 — Microbial Growth", "content": "Binary fission..."}],
        "generate_study_guide": true,
        "extracted_tasks": ["Review Lab 6 worksheet"],
        "extracted_events": [{"title": "Exam 3", "date": "2026-04-15"}]
    }"""
    with patch("agent.classifier.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = _mock_response(json_str)
        result = classify("some microbio content", config)

    assert isinstance(result, ClassificationResult)
    assert result.destination == "microbiology"
    assert len(result.chapters) == 1
    assert result.chapters[0].title == "Chapter 6 — Microbial Growth"
    assert result.generate_study_guide is True
    assert result.extracted_tasks == ["Review Lab 6 worksheet"]
    assert result.extracted_events[0]["date"] == "2026-04-15"

def test_classify_falls_back_on_bad_json(config):
    with patch("agent.classifier.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = _mock_response("not json")
        result = classify("content", config)

    assert result.destination == "mind_vault"
    assert result.chapters[0].title == "Unclassified"

def test_classify_multi_chapter(config):
    json_str = """{
        "destination": "nurs_2030",
        "chapters": [
            {"title": "Chapter 3 — Safety", "content": "Safety content"},
            {"title": "Chapter 4 — Ethics", "content": "Ethics content"}
        ],
        "generate_study_guide": false,
        "extracted_tasks": [],
        "extracted_events": []
    }"""
    with patch("agent.classifier.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = _mock_response(json_str)
        result = classify("nursing content", config)

    assert len(result.chapters) == 2
    assert result.destination == "nurs_2030"
