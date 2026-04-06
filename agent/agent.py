"""
agent.py — JPATE Triage Agent
Run: python agent/agent.py
Polls Notion Inbox every POLL_INTERVAL seconds. Ctrl+C to stop.
"""
import logging
import logging.handlers
import time
from pathlib import Path

from agent.config import load_config
from agent.notion import NotionClient
from agent.classifier import classify
from agent.router import route
from agent.sync import run_sync_cycle

LOG_PATH = Path(__file__).parent / "logs" / "agent.log"


def _setup_logging() -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[handler, logging.StreamHandler()],
    )


def process_inbox(notion: NotionClient, config) -> int:
    """Check Inbox for new pages and process each. Returns count processed."""
    pages = notion.get_child_pages(config.notion_inbox_page_id)
    unprocessed = [p for p in pages if not p["title"].startswith("✅")]

    for page in unprocessed:
        logging.info("Processing: %s", page["title"])
        try:
            content = notion.get_page_text(page["id"])
            result = classify(content, config)
            logging.info(
                "Classified as '%s' — %d chapter(s)", result.destination, len(result.chapters)
            )
            route(result, notion, config)
            # Title update is last — if it fails, page re-enters queue next cycle.
            # route() may run twice for the same page in that case (creates duplicates).
            # Acceptable for a single-user agent; fix with a staging title if it becomes an issue.
            notion.update_page_title(page["id"], f"✅ {page['title']}")
            logging.info("Done: %s", page["title"])
        except Exception as exc:
            logging.error("Failed to process '%s': %s", page["title"], exc, exc_info=True)

    return len(unprocessed)


def run_forever(notion: NotionClient, config) -> None:
    logging.info("Agent started. Polling every %ds.", config.poll_interval)
    while True:
        try:
            count = process_inbox(notion, config)
            if count:
                logging.info("Triage: processed %d item(s).", count)
            run_sync_cycle(notion, config)
        except Exception as exc:
            logging.error("Cycle error: %s", exc, exc_info=True)
        time.sleep(config.poll_interval)


def main() -> None:
    _setup_logging()
    config = load_config()
    notion = NotionClient(config.notion_token)
    run_forever(notion, config)


if __name__ == "__main__":
    main()
