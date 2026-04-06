import pytest
from unittest.mock import MagicMock, patch
from agent.notion import NotionClient

@pytest.fixture
def client():
    with patch("agent.notion.Client") as MockClient:
        nc = NotionClient("secret_token")
        nc._client = MockClient.return_value
        yield nc

def test_get_child_pages_returns_list(client):
    client._client.blocks.children.list.return_value = {
        "results": [
            {"type": "child_page", "id": "page-1", "child_page": {"title": "My Notes"}},
            {"type": "paragraph", "id": "block-2"},  # non-page block, should be skipped
        ],
        "has_more": False,
    }
    pages = client.get_child_pages("parent-id")
    assert pages == [{"id": "page-1", "title": "My Notes"}]

def test_extract_text_from_blocks(client):
    blocks = [
        {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "Hello world"}]}},
        {"type": "heading_1", "heading_1": {"rich_text": [{"plain_text": "A Heading"}]}},
        {"type": "to_do", "to_do": {"rich_text": [{"plain_text": "Do this"}], "checked": False}},
    ]
    text = client.extract_text(blocks)
    assert "Hello world" in text
    assert "A Heading" in text
    assert "Do this" in text

def test_get_todo_blocks_filters_correctly(client):
    client._client.blocks.children.list.return_value = {
        "results": [
            {"type": "to_do", "id": "todo-1", "to_do": {"rich_text": [{"plain_text": "Buy milk"}], "checked": False}},
            {"type": "to_do", "id": "todo-2", "to_do": {"rich_text": [{"plain_text": "Done task"}], "checked": True}},
            {"type": "paragraph", "id": "p-1", "paragraph": {"rich_text": [{"plain_text": "not a todo"}]}},
        ],
        "has_more": False,
    }
    todos = client.get_todo_blocks("page-id")
    assert len(todos) == 2
    assert todos[0] == {"id": "todo-1", "text": "Buy milk", "checked": False}
    assert todos[1] == {"id": "todo-2", "text": "Done task", "checked": True}

def test_create_child_page_returns_id(client):
    client._client.pages.create.return_value = {"id": "new-page-id"}
    page_id = client.create_child_page("parent-id", "Chapter 6 — Growth", [])
    assert page_id == "new-page-id"
    client._client.pages.create.assert_called_once()

def test_update_page_title(client):
    client.update_page_title("page-id", "✅ My Notes")
    client._client.pages.update.assert_called_once_with(
        page_id="page-id",
        properties={"title": [{"text": {"content": "✅ My Notes"}}]}
    )
