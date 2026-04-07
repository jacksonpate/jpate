"""Runtime configuration for the Notion Triage Agent, loaded from environment variables."""
from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    notion_token: str
    notion_inbox_page_id: str
    anthropic_api_key: str
    google_calendar_id: str
    jpate_root: Path
    poll_interval: int
    # Hard-coded destination IDs from spec
    microbio_page_id: str = "be4e45005934493f88b6ddfa03113674"
    nurs2030_page_id: str = "ae3d9ad3d83141c6a9e56e36fe000d42"
    nurs2040_page_id: str = "c9511e785e0841eeb9ef8f34c47515d9"
    task_manager_id: str = "a861e1550b514fe8a532344bb1fd0036"
    calendar_db_id: str = "2b7cdb62-749e-4c9c-b7c3-e83f79f86707"
    mind_vault_id: str = "10211b8f4baf4d829e49df1b6b9ce22d"
    dashboard_id: str = "31c89913b6418033b240f6e34a11382f"
    academic_hub_id: str = "a63940ef072349eda57e59771853e745"


def load_config() -> Config:
    # load_dotenv here (not at module level) keeps test isolation clean
    load_dotenv(Path(__file__).parent.parent / ".env")
    return Config(
        notion_token=os.environ["NOTION_TOKEN"],
        notion_inbox_page_id=os.environ["NOTION_INBOX_PAGE_ID"],
        anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
        # Defaults to "primary" (Google Calendar API sentinel for user's default calendar)
        google_calendar_id=os.environ.get("GOOGLE_CALENDAR_ID", "primary"),
        # Default is Jackson's local machine path — override via JPATE_ROOT in .env
        jpate_root=Path(os.environ.get("JPATE_ROOT", "C:/Users/jacks/JPATE")),
        poll_interval=int(os.environ.get("POLL_INTERVAL", "60")),
    )
