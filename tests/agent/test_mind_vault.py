import pytest
from unittest.mock import MagicMock, patch
from agent.handlers.mind_vault import dump_to_mind_vault, update_active_situations

@pytest.fixture
def notion():
    return MagicMock()

@pytest.fixture
def config():
    cfg = MagicMock()
    cfg.mind_vault_id = "mind-vault-id"
    cfg.anthropic_api_key = "sk-ant-test"
    return cfg

def test_dump_to_mind_vault_creates_page(notion, config):
    notion.create_child_page.return_value = "new-page-id"
    dump_to_mind_vault("My Note", "Note content here", notion, config)
    notion.create_child_page.assert_called_once()
    call_args = notion.create_child_page.call_args
    assert call_args[0][0] == "mind-vault-id"
    assert call_args[0][1] == "My Note"

def test_dump_with_review_flag_adds_warning_callout(notion, config):
    notion.create_child_page.return_value = "p"
    dump_to_mind_vault("Title", "Content", notion, config, needs_review=True)
    blocks = notion.create_child_page.call_args[0][2]
    callout_block = blocks[0]
    assert callout_block["type"] == "callout"
    assert "⚠️" in callout_block["callout"]["icon"]["emoji"]

def test_update_active_situations_appends_blocks(notion, config):
    open_tasks = ["Study Lab 6", "AceMapp due May 5"]
    with patch("agent.handlers.mind_vault.anthropic.Anthropic") as MockAnth:
        MockAnth.return_value.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Active: studying for Microbio, completing AceMapp")]
        )
        update_active_situations(open_tasks, notion, config)
    notion.append_blocks.assert_called_once()
