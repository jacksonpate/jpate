import json
import logging
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

_SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _get_gcal_service(jpate_root: Path):
    token_path = jpate_root / "token.json"
    if not token_path.exists():
        raise FileNotFoundError(
            f"Google Calendar token not found at {token_path}. "
            "Run the one-time OAuth setup in Task 7."
        )
    creds = Credentials.from_authorized_user_info(
        json.loads(token_path.read_text()), _SCOPES
    )
    return build("calendar", "v3", credentials=creds)


def create_event(title: str, date: str, notion, config) -> None:
    """
    Create an event in both Notion Calendar DB and Google Calendar.
    date must be ISO format: YYYY-MM-DD
    """
    # Notion Calendar DB
    notion.create_calendar_db_entry(config.calendar_db_id, title, date)

    # Google Calendar
    try:
        service = _get_gcal_service(config.jpate_root)
        event = {
            "summary": title,
            "start": {"date": date, "timeZone": "America/Chicago"},
            "end": {"date": date, "timeZone": "America/Chicago"},
        }
        service.events().insert(calendarId=config.google_calendar_id, body=event).execute()
    except Exception as exc:
        logger.exception("Google Calendar write failed for '%s'", title)
        # Notion write already succeeded — log and continue
