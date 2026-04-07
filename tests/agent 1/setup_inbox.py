"""
One-time setup: creates the Inbox page under Jackson Pate root.
Run: python agent/setup_inbox.py
Copy the printed page ID into .env as NOTION_INBOX_PAGE_ID=
"""
from agent.config import load_config
from agent.notion import NotionClient

DASHBOARD_ID = "31c89913b6418033b240f6e34a11382f"


def main():
    config = load_config()
    notion = NotionClient(config.notion_token)
    page_id = notion.create_child_page(
        DASHBOARD_ID,
        "📥 Inbox",
        [{"type": "callout", "callout": {
            "icon": {"type": "emoji", "emoji": "📥"},
            "rich_text": [{"type": "text", "text": {"content": "Share Notability exports here."}}]
        }}]
    )
    print(f"\nInbox page created!")
    print(f"NOTION_INBOX_PAGE_ID={page_id}")
    print("\nAdd this to your .env file.")


if __name__ == "__main__":
    main()
