import os
import pytest
from agent.config import load_config

def test_load_config_reads_env(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "secret_abc")
    monkeypatch.setenv("NOTION_INBOX_PAGE_ID", "inbox-id-123")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-abc")
    monkeypatch.setenv("GOOGLE_CALENDAR_ID", "primary")
    monkeypatch.setenv("JPATE_ROOT", "C:/Users/jacks/JPATE")
    monkeypatch.setenv("POLL_INTERVAL", "30")

    config = load_config()

    assert config.notion_token == "secret_abc"
    assert config.notion_inbox_page_id == "inbox-id-123"
    assert config.anthropic_api_key == "sk-ant-abc"
    assert config.poll_interval == 30

def test_load_config_defaults(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "t")
    monkeypatch.setenv("NOTION_INBOX_PAGE_ID", "i")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    monkeypatch.setenv("GOOGLE_CALENDAR_ID", "primary")
    monkeypatch.delenv("POLL_INTERVAL", raising=False)
    monkeypatch.delenv("JPATE_ROOT", raising=False)

    config = load_config()
    assert config.poll_interval == 60

def test_load_config_missing_required(monkeypatch):
    monkeypatch.delenv("NOTION_TOKEN", raising=False)
    with pytest.raises(KeyError):
        load_config()
