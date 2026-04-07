"""
agent.py — JPATE Triage Agent
Run: python agent/agent.py
Polls Notion Inbox every POLL_INTERVAL seconds. Ctrl+C to stop.
"""
import base64
import io
import logging
import logging.handlers
import sys
import time
from pathlib import Path

import anthropic
import httpx
from pypdf import PdfReader

from agent.config import load_config
from agent.notion import NotionClient
from agent.classifier import classify
from agent.router import route
from agent.sync import run_sync_cycle

LOG_PATH = Path(__file__).parent / "logs" / "agent.log"


def _setup_logging() -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    stream_handler = logging.StreamHandler(
        stream=open(sys.stdout.fileno(), mode="w", encoding="utf-8", closefd=False)
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[file_handler, stream_handler],
    )


def _extract_pdf_text(url: str) -> str:
    """Download a PDF from url and return extracted text."""
    resp = httpx.get(url, follow_redirects=True, timeout=30)
    resp.raise_for_status()
    reader = PdfReader(io.BytesIO(resp.content))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


_IMAGE_EXTRACT_PROMPT = (
    "Extract all text visible in this image exactly as written. "
    "Then describe any diagrams, charts, or figures. "
    "Output raw content only — no commentary, no formatting."
)

_MEDIA_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp",
}


def _extract_image_text(url: str, config) -> str:
    """Download an image and use Claude vision to extract its content."""
    resp = httpx.get(url, follow_redirects=True, timeout=30)
    resp.raise_for_status()
    # Detect media type from Content-Type header, fall back to URL extension
    content_type = resp.headers.get("content-type", "").split(";")[0].strip()
    if not content_type or content_type == "application/octet-stream":
        ext = "." + url.split("?")[0].rsplit(".", 1)[-1].lower()
        content_type = _MEDIA_TYPES.get(ext, "image/png")
    data = base64.standard_b64encode(resp.content).decode()
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": content_type, "data": data}},
            {"type": "text", "text": _IMAGE_EXTRACT_PROMPT},
        ]}],
    )
    return msg.content[0].text.strip() if msg.content else ""


def process_inbox(notion: NotionClient, config) -> int:
    """Check Inbox for new pages and PDF uploads. Returns count processed."""
    count = 0

    # Child pages (text notes)
    pages = notion.get_child_pages(config.notion_inbox_page_id)
    for page in [p for p in pages if not p["title"].startswith("✅")]:
        logging.info("Processing page: %s", page["title"])
        try:
            content = notion.get_page_text(page["id"])
            result = classify(content, config)
            logging.info("Classified as '%s' — %d chapter(s)", result.destination, len(result.chapters))
            route(result, notion, config)
            notion.update_page_title(page["id"], f"✅ {page['title']}")
            logging.info("Done: %s", page["title"])
            count += 1
        except Exception as exc:
            logging.error("Failed to process page '%s': %s", page["title"], exc, exc_info=True)

    # PDF uploads
    pdfs = notion.get_pdf_blocks(config.notion_inbox_page_id)
    for pdf in pdfs:
        logging.info("Processing PDF: %s", pdf["name"])
        try:
            content = _extract_pdf_text(pdf["url"])
            if not content.strip():
                logging.warning("PDF '%s' yielded no text — skipping", pdf["name"])
                notion.delete_block(pdf["id"])
                continue
            result = classify(content, config)
            logging.info("Classified as '%s' — %d chapter(s)", result.destination, len(result.chapters))
            try:
                route(result, notion, config)
            except Exception as exc:
                logging.error("Route failed for PDF '%s': %s", pdf["name"], exc, exc_info=True)
            notion.delete_block(pdf["id"])
            logging.info("Done (deleted PDF block): %s", pdf["name"])
            count += 1
        except Exception as exc:
            logging.error("Failed to process PDF '%s': %s", pdf["name"], exc, exc_info=True)

    # Image uploads (screenshots, photos of notes/slides)
    images = notion.get_image_blocks(config.notion_inbox_page_id)
    for img in images:
        logging.info("Processing image: %s", img["name"])
        try:
            content = _extract_image_text(img["url"], config)
            if not content.strip():
                logging.warning("Image '%s' yielded no content — skipping", img["name"])
                notion.delete_block(img["id"])
                continue
            result = classify(content, config)
            logging.info("Classified as '%s' — %d chapter(s)", result.destination, len(result.chapters))
            try:
                route(result, notion, config)
            except Exception as exc:
                logging.error("Route failed for image '%s': %s", img["name"], exc, exc_info=True)
            notion.delete_block(img["id"])
            logging.info("Done (deleted image block): %s", img["name"])
            count += 1
        except Exception as exc:
            logging.error("Failed to process image '%s': %s", img["name"], exc, exc_info=True)

    return count


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
