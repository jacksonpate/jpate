from dataclasses import dataclass, field
import json
import anthropic


@dataclass
class Chapter:
    title: str
    content: str


@dataclass
class ClassificationResult:
    destination: str
    chapters: list[Chapter]
    generate_study_guide: bool
    extracted_tasks: list[str] = field(default_factory=list)
    extracted_events: list[dict] = field(default_factory=list)


_PROMPT = """\
You are classifying content for a nursing student at Auburn University.
Content may be Notability exports, screenshots of Canvas, syllabi, or phone photos of notes/slides.

Classes: Microbiology (BIOL3200), NURS 2030 (Foundations of Professional Nursing), NURS 2040.

Analyze the content and return ONLY a JSON object with this exact structure:
{
  "destination": "microbiology | nurs_2030 | nurs_2040 | tasks | calendar | mind_vault",
  "chapters": [{"title": "Chapter N — Descriptive Title", "content": "full chapter text"}],
  "generate_study_guide": true or false,
  "extracted_tasks": ["actionable to-do items only"],
  "extracted_events": [{"title": "event name", "date": "YYYY-MM-DD"}]
}

Rules:
- destination: pick the single best match.
  - If content is primarily a list of assignments, due dates, or a course schedule → "calendar"
  - If content is primarily a to-do list or action items with no course content → "tasks"
  - Use "mind_vault" only if content is truly unclassifiable.
- chapters: for calendar/task destinations, use one chapter summarizing what was found.
- generate_study_guide: true only for lecture notes, lab content, exam prep material.
- extracted_tasks: ALL assignments, deadlines, and actionable items. Always populate this if any due dates or assignments are visible, even partially.
- extracted_events: items with a specific date — overlap with extracted_tasks is expected and correct.
- Return ONLY the JSON object. No markdown, no explanation.

Content:
"""


def classify(content: str, config) -> ClassificationResult:
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": _PROMPT + content}],
    )
    raw = message.content[0].text.strip()
    try:
        data = json.loads(raw)
        return ClassificationResult(
            destination=data["destination"],
            chapters=[Chapter(**c) for c in data["chapters"]],
            generate_study_guide=bool(data.get("generate_study_guide", False)),
            extracted_tasks=data.get("extracted_tasks", []),
            extracted_events=data.get("extracted_events", []),
        )
    except (json.JSONDecodeError, KeyError, TypeError):
        return ClassificationResult(
            destination="mind_vault",
            chapters=[Chapter(title="Unclassified", content=content)],
            generate_study_guide=False,
        )
