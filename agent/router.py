from agent.classifier import ClassificationResult
from agent.handlers.study import create_chapter_pages
from agent.handlers.tasks import append_tasks
from agent.handlers.calendar import create_event
from agent.handlers.mind_vault import dump_to_mind_vault

_DESTINATION_PAGE = {
    "microbiology": "microbio_page_id",
    "nurs_2030": "nurs2030_page_id",
    "nurs_2040": "nurs2040_page_id",
}


def route(result: ClassificationResult, notion, config) -> None:
    """Dispatch a ClassificationResult to the appropriate handlers."""

    # Route main content
    if result.destination in _DESTINATION_PAGE:
        parent_id = getattr(config, _DESTINATION_PAGE[result.destination])
        create_chapter_pages(
            result.chapters, parent_id, result.generate_study_guide, notion, config
        )
    elif result.destination == "mind_vault":
        content = "\n\n".join(c.content for c in result.chapters)
        title = result.chapters[0].title if result.chapters else "Untitled"
        dump_to_mind_vault(title, content, notion, config)

    # Always route extracted tasks to Task Manager
    if result.extracted_tasks:
        append_tasks(result.extracted_tasks, notion, config)

    # Always route extracted events to Calendar
    for event in result.extracted_events:
        create_event(event["title"], event["date"], notion, config)
