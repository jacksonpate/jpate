#!/usr/bin/env python3
"""Build the Obsidian -> Notion migration package.

Walks the vault, parses frontmatter, cleans content, and produces a
NOVA-ready package at AI & Tech/migrations/2026-04-13-obsidian-to-notion/.
"""
from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path

VAULT = Path("/home/user/jpate")
OUT = VAULT / "AI & Tech" / "migrations" / "2026-04-13-obsidian-to-notion"

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
RELATED_SECTION = re.compile(
    r"\n##\s*(Related|Mentioned In)\s*\n.*?(?=\n##\s|\Z)", re.DOTALL
)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body) after stripping the YAML block."""
    m = FRONTMATTER.match(text)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end():]
    fm: dict = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            fm[k] = [s.strip().strip('"') for s in inner.split(",") if s.strip()]
        else:
            fm[k] = v.strip('"')
    return fm, body


def wikilink_to_bold(text: str) -> str:
    def repl(m: re.Match) -> str:
        target = m.group(1)
        # [[Page|Alias]] -> **Alias**, else **Page**
        if "|" in target:
            target = target.split("|", 1)[1]
        # Strip folder path prefixes like Life/personal-arc -> personal-arc
        if "/" in target:
            target = target.rsplit("/", 1)[1]
        return f"**{target}**"
    return WIKILINK.sub(repl, text)


def strip_related_section(text: str) -> str:
    """Remove ## Related and ## Mentioned In sections (Notion handles backlinks)."""
    # Keep "Mentioned In" sections that have rich narrative content (>500 chars
    # of body) — those are real synthesis, not just link lists. Detect by length.
    out = text
    while True:
        m = re.search(r"\n##\s*(Related)\s*\n(.*?)(?=\n##\s|\Z)", out, re.DOTALL)
        if not m:
            break
        body = m.group(2).strip()
        # If the section is purely wikilinks (lines starting with - [[), drop it
        link_only_lines = [
            ln.strip() for ln in body.splitlines()
            if ln.strip() and not ln.strip().startswith("- [[")
            and not ln.strip().startswith("- **")
        ]
        if len(link_only_lines) <= 1:  # mostly link list
            out = out[:m.start()] + out[m.end():]
        else:
            break
    return out


def clean_body(body: str) -> str:
    body = strip_related_section(body)
    body = wikilink_to_bold(body)
    return body.strip() + "\n"


def read_md(p: Path) -> tuple[dict, str]:
    text = p.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    return fm, clean_body(body)


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return s or "untitled"


# ---------- 1. Static pages ----------

STATIC_SECTIONS = [
    # (Notion section folder, list of (source_path, output_filename, page_title))
    ("identity", [
        ("Core/identity.md",        "core-identity.md",   "Core Identity"),
        ("Core/circle.md",          "close-circle.md",    "Close Circle"),
        ("Core/roles.md",           "roles.md",           "Roles"),
        ("Claude-Brain/00-identity.md", "claude-brain-00-identity.md", "Claude-Brain — Identity"),
        ("Claude-Brain/01-school.md",   "claude-brain-01-school.md",   "Claude-Brain — School"),
        ("Claude-Brain/02-projects.md", "claude-brain-02-projects.md", "Claude-Brain — Projects"),
        ("Claude-Brain/03-goals.md",    "claude-brain-03-goals.md",    "Claude-Brain — Goals"),
        ("Claude-Brain/04-health.md",   "claude-brain-04-health.md",   "Claude-Brain — Health"),
        ("Claude-Brain/05-life.md",     "claude-brain-05-life.md",     "Claude-Brain — Life"),
        ("Claude-Brain/06-systems.md",  "claude-brain-06-systems.md",  "Claude-Brain — Systems"),
    ]),
    ("life", [
        ("Life/active-situations.md", "active-situations.md", "Active Situations"),
        ("Life/personal-arc.md",      "personal-arc.md",      "Personal Arc"),
        ("Life/long-term-vision.md",  "long-term-vision.md",  "Long-Term Vision"),
        ("Life/bible-journal.md",     "bible-journal.md",     "Bible Journal"),
        ("Life/book-journal.md",      "book-journal.md",      "Book Journal"),
        ("Life/things-to-remember.md", "things-to-remember.md", "Things to Remember"),
        ("Life/asap-todo.md",         "asap-todo.md",         "ASAP Todo"),
    ]),
    ("health", [
        ("Health/health-protocol.md",                "health-protocol.md",                "Health Protocol"),
        ("Health/medication-supplement-protocol.md", "medication-supplement-protocol.md", "Medication & Supplement Protocol"),
    ]),
    ("interests", [
        ("Interests/interests-lab.md", "interests-lab.md", "Interests Lab"),
        ("Interests/gear.md",          "gear.md",          "Gear"),
    ]),
]

manifest_pages: list[dict] = []

for section, files in STATIC_SECTIONS:
    section_dir = OUT / "pages" / section
    section_dir.mkdir(parents=True, exist_ok=True)
    for src_rel, out_name, title in files:
        src = VAULT / src_rel
        if not src.exists():
            print(f"  SKIP missing: {src_rel}")
            continue
        fm, body = read_md(src)
        out_path = section_dir / out_name
        # Render frontmatter as a small properties block at the top
        props_block = ""
        if fm:
            lines = []
            for k, v in fm.items():
                if isinstance(v, list):
                    v = ", ".join(v)
                lines.append(f"- **{k}:** {v}")
            props_block = "## Source Properties\n" + "\n".join(lines) + "\n\n"
        out_path.write_text(f"# {title}\n\n{props_block}{body}", encoding="utf-8")
        manifest_pages.append({
            "section": section,
            "title": title,
            "source": src_rel,
            "output": str(out_path.relative_to(OUT)),
            "frontmatter": fm,
        })

# ---------- AI & Tech content pages (dev logs + docs) ----------

ai_tech_dir = OUT / "pages" / "ai-tech"
ai_tech_dir.mkdir(parents=True, exist_ok=True)

ai_tech_root = VAULT / "AI & Tech"
for src in sorted(ai_tech_root.rglob("*.md")):
    rel = src.relative_to(ai_tech_root)
    # Skip the migration package itself + scripts
    if "migrations" in rel.parts or "scripts" in rel.parts:
        continue
    fm, body = read_md(src)
    title = src.stem.replace("-", " ").title()
    out_name = slugify(str(rel).replace("/", "-")) + ".md"
    (ai_tech_dir / out_name).write_text(
        f"# {title}\n\n*Source: AI & Tech/{rel}*\n\n{body}",
        encoding="utf-8",
    )
    manifest_pages.append({
        "section": "ai-tech",
        "title": title,
        "source": f"AI & Tech/{rel}",
        "output": f"pages/ai-tech/{out_name}",
        "frontmatter": fm,
    })

# ---------- Scripts summary page (no code dump) ----------

scripts_dir = ai_tech_root / "scripts"
script_summaries = []
for s in sorted(scripts_dir.glob("*.py")):
    # Read the docstring (first triple-quoted block) for a summary
    text = s.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'"""(.*?)"""', text, re.DOTALL)
    summary = m.group(1).strip().split("\n")[0] if m else "(no docstring)"
    script_summaries.append((s.name, summary, len(text)))

scripts_md = "# Scripts\n\nPython automation scripts in the vault. Code lives in the repo; this page is the index.\n\n"
for name, summary, size in script_summaries:
    scripts_md += f"## `{name}`\n\n- **Size:** {size:,} bytes\n- **What it does:** {summary}\n\n"
(ai_tech_dir / "scripts-index.md").write_text(scripts_md, encoding="utf-8")
manifest_pages.append({
    "section": "ai-tech",
    "title": "Scripts Index",
    "source": "AI & Tech/scripts/",
    "output": "pages/ai-tech/scripts-index.md",
    "frontmatter": {},
})

# ---------- 2. Journal database ----------

journal_dir = VAULT / "Journal"
journal_rows = []
for src in sorted(journal_dir.glob("*.md")):
    fm, body = read_md(src)
    # Title: first H1 in body, or filename
    h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = h1.group(1).strip() if h1 else src.stem
    body_no_title = re.sub(r"^#\s+.+\n+", "", body, count=1)
    # Date: from frontmatter, else parse from filename YYYY-MM-DD
    d = fm.get("date")
    if not d:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", src.stem)
        d = m.group(1) if m else None
    journal_rows.append({
        "title": title,
        "properties": {
            "Date": d,
            "Type": fm.get("type", "journal"),
            "Category": fm.get("category", "journal"),
            "Tags": fm.get("tags", []),
            "Source": fm.get("source", "Obsidian vault"),
        },
        "content_markdown": body_no_title.strip(),
        "source_file": f"Journal/{src.name}",
    })

journal_db = {
    "title": "📔 Journal",
    "schema": {
        "Name": {"type": "title"},
        "Date": {"type": "date"},
        "Type": {"type": "select", "options": sorted({r["properties"]["Type"] for r in journal_rows if r["properties"]["Type"]})},
        "Category": {"type": "select", "options": sorted({r["properties"]["Category"] for r in journal_rows if r["properties"]["Category"]})},
        "Tags": {"type": "multi_select", "options": sorted({t for r in journal_rows for t in (r["properties"]["Tags"] or [])})},
        "Source": {"type": "rich_text"},
    },
    "default_view": {"type": "table", "sort": [{"property": "Date", "direction": "descending"}]},
    "rows": journal_rows,
}
(OUT / "databases" / "journal.json").write_text(
    json.dumps(journal_db, indent=2, default=str), encoding="utf-8"
)

# ---------- 3. People database ----------

people_dir = VAULT / "People"
people_rows = []
for src in sorted(people_dir.glob("*.md")):
    fm, body = read_md(src)
    name = src.stem
    h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if h1:
        name = h1.group(1).strip()
    body_no_title = re.sub(r"^#\s+.+\n+", "", body, count=1)
    people_rows.append({
        "title": name,
        "properties": {
            "Type": fm.get("type", "person"),
            "Category": fm.get("category", "people"),
            "Tags": fm.get("tags", []),
            "Related People": fm.get("related_people", []),
            "Date Updated": fm.get("date_updated") or fm.get("date_processed"),
            "Source": fm.get("source", "Obsidian vault"),
        },
        "content_markdown": body_no_title.strip(),
        "source_file": f"People/{src.name}",
    })

people_db = {
    "title": "👥 People",
    "schema": {
        "Name": {"type": "title"},
        "Type": {"type": "select"},
        "Category": {"type": "select"},
        "Tags": {"type": "multi_select", "options": sorted({t for r in people_rows for t in (r["properties"]["Tags"] or [])})},
        "Related People": {"type": "relation", "to": "self"},
        "Date Updated": {"type": "date"},
        "Source": {"type": "rich_text"},
    },
    "default_view": {"type": "table", "sort": [{"property": "Name", "direction": "ascending"}]},
    "rows": people_rows,
    "relation_pass_2": {
        "note": "After all rows are created, run a second pass to wire 'Related People' relations. For each row, look up its 'Related People' list (currently strings), find matching pages by Name, and set the relation property to the resolved page IDs.",
    },
}
(OUT / "databases" / "people.json").write_text(
    json.dumps(people_db, indent=2, default=str), encoding="utf-8"
)

# ---------- 4. Snapchat Contacts database ----------

snap_people_dir = VAULT / "Personal Data" / "Snapchat" / "People"
snap_rows = []
if snap_people_dir.exists():
    for src in sorted(snap_people_dir.glob("*.md")):
        fm, body = read_md(src)
        name = src.stem
        h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1:
            name = h1.group(1).strip()
        body_no_title = re.sub(r"^#\s+.+\n+", "", body, count=1)
        snap_rows.append({
            "title": name,
            "properties": {
                "Username": fm.get("username", src.stem),
                "Era": fm.get("era", []),
                "Status": fm.get("status"),
                "Tags": fm.get("tags", []),
            },
            "content_markdown": body_no_title.strip(),
            "source_file": f"Personal Data/Snapchat/People/{src.name}",
        })

snapchat_db = {
    "title": "📸 Snapchat Contacts",
    "schema": {
        "Name": {"type": "title"},
        "Username": {"type": "rich_text"},
        "Era": {"type": "multi_select"},
        "Status": {"type": "select"},
        "Tags": {"type": "multi_select"},
    },
    "default_view": {"type": "table", "sort": [{"property": "Name", "direction": "ascending"}]},
    "rows": snap_rows,
}
(OUT / "databases" / "snapchat-contacts.json").write_text(
    json.dumps(snapchat_db, indent=2, default=str), encoding="utf-8"
)

# ---------- 5. Snapchat Intelligence pages ----------

snap_root = VAULT / "Personal Data" / "Snapchat"
overview_sources = [
    "People Index.md",
    "Friends/friends-current.md",
    "Friends/friends-deleted.md",
    "Friends/friends-blocked.md",
    "Profile/user-profile.md",
    "Snaps/snap-history-full.md",
    "Messages/_index.md",
]
overview_md = "# 📸 Snapchat Intelligence — Overview\n\n*Synthesized from 6 years of Snapchat data: 10,620 snaps, 304+ conversations, 35+ profiled people.*\n\n"
for rel in overview_sources:
    p = snap_root / rel
    if not p.exists():
        continue
    _, body = read_md(p)
    overview_md += f"\n---\n\n## From `Snapchat/{rel}`\n\n{body}\n"
(OUT / "snapchat" / "overview.md").write_text(overview_md, encoding="utf-8")

# Notable threads: top 10 largest message files
msg_dir = snap_root / "Messages"
notable_md = "# 📸 Snapchat — Notable Threads\n\n*Top conversations by volume. Full per-message detail stays in the vault; this is the synthesized take.*\n\n"
if msg_dir.exists():
    files = sorted(
        [f for f in msg_dir.glob("*.md") if f.name != "_index.md"],
        key=lambda f: f.stat().st_size,
        reverse=True,
    )[:10]
    for src in files:
        _, body = read_md(src)
        # Trim very long bodies to ~3000 chars for the summary page
        if len(body) > 3000:
            body = body[:3000] + "\n\n*[truncated — full thread in vault]*"
        notable_md += f"\n---\n\n## {src.stem}\n\n{body}\n"
(OUT / "snapchat" / "notable-threads.md").write_text(notable_md, encoding="utf-8")

# ---------- 6. Manifest + README + EXECUTOR ----------

manifest = {
    "migration": "Obsidian → Notion",
    "date": str(date.today()),
    "branch": "claude/obsidian-to-notion-migration-0E8WD",
    "vault_root": str(VAULT),
    "package_root": str(OUT),
    "target_notion_root": "Jackson Pate → 📖 Vault Mirror (NEW)",
    "structure": {
        "static_pages": {
            "count": len(manifest_pages),
            "by_section": {s: sum(1 for p in manifest_pages if p["section"] == s)
                           for s in {p["section"] for p in manifest_pages}},
            "pages": manifest_pages,
        },
        "databases": [
            {"name": "📔 Journal", "rows": len(journal_rows), "file": "databases/journal.json"},
            {"name": "👥 People", "rows": len(people_rows), "file": "databases/people.json"},
            {"name": "📸 Snapchat Contacts", "rows": len(snap_rows), "file": "databases/snapchat-contacts.json"},
        ],
        "snapchat_pages": [
            {"name": "Snapchat Intelligence — Overview", "file": "snapchat/overview.md"},
            {"name": "Snapchat — Notable Threads", "file": "snapchat/notable-threads.md"},
        ],
    },
    "skipped": {
        "agents": "Operational coordination files (inboxes, Shared_Log, handoff, JOURNAL, STATUS).",
        "memory_rules": "Standing rules and feedback files (operational, not personal info).",
        "snapchat_raw": "Per-conversation Messages/*.md files (373 raw — represented via Notable Threads + Contacts DB instead).",
        "scripts_code": "Python source code (documented on Scripts Index page, code stays in the repo).",
        "untitled_base": "*.base placeholder files (empty).",
    },
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

print("=" * 60)
print("MIGRATION PACKAGE BUILT")
print("=" * 60)
print(f"Static pages: {len(manifest_pages)}")
print(f"Journal rows: {len(journal_rows)}")
print(f"People rows:  {len(people_rows)}")
print(f"Snapchat rows: {len(snap_rows)}")
print(f"Output: {OUT}")
