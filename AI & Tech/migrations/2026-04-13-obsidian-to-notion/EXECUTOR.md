# EXECUTOR — Obsidian → Notion Migration

**For:** NOVA agent (or any session with Notion MCP connected)
**Package:** `AI & Tech/migrations/2026-04-13-obsidian-to-notion/`
**Target:** Jackson Pate workspace → new `📖 Vault Mirror` root page

This document is the runbook. Follow phases in order. Each phase is small enough to
checkpoint and resume.

---

## Tools required

All from `mcp__claude_ai_Notion__*`:
- `notion-search` — collision-check existing pages
- `notion-fetch` — confirm page IDs after creation
- `notion-create-pages` — bulk page creation (prefer batches of 5–10)
- `notion-create-database` — the 3 databases
- `notion-update-page` — populate database rows, set relations
- `notion-create-view` — sorted default views

---

## Phase 1 — Discovery (read-only, ~5 calls)

Search Notion for collisions before creating anything. For each query, record any
matching page IDs:

```
notion-search query="Vault Mirror"
notion-search query="Journal" type="database"
notion-search query="People" type="database"
notion-search query="Snapchat"
notion-search query="Active Situations"
```

Decision tree:
- If `📖 Vault Mirror` does not exist → create fresh in Phase 2
- If a database with the same name exists → archive or rename it before Phase 4
- If individual pages from the 2026-04-07 migration exist (Health Protocol, Interests
  Lab, etc.) → migrate the new content as **subpages or separate pages under
  📖 Vault Mirror** to avoid clobbering. Do NOT update-in-place unless asked.

---

## Phase 2 — Skeleton

### 2a. Create the root page

```
notion-create-pages parent=<Jackson Pate workspace root> pages=[{
  title: "📖 Vault Mirror",
  emoji: "📖",
  content: "Single entry point for the Obsidian vault mirror migrated 2026-04-13.
            See sub-pages and databases below."
}]
```

Record the returned page ID as `VAULT_MIRROR_ID`.

### 2b. Create the 5 section pages under Vault Mirror

```
notion-create-pages parent=VAULT_MIRROR_ID pages=[
  { title: "🧠 Identity",            emoji: "🧠" },
  { title: "🔥 Life",                 emoji: "🔥" },
  { title: "💪 Health",               emoji: "💪" },
  { title: "🧪 Interests",            emoji: "🧪" },
  { title: "🤖 AI & Tech",            emoji: "🤖" },
  { title: "📸 Snapchat Intelligence", emoji: "📸" },
]
```

Record IDs as `IDENTITY_ID`, `LIFE_ID`, `HEALTH_ID`, `INTERESTS_ID`, `AI_TECH_ID`,
`SNAPCHAT_ID`.

### 2c. Create the 3 databases

For each database, read its `databases/*.json` file in the package, then call
`notion-create-database` with the schema and parent. Databases sit at the root of
`📖 Vault Mirror` (so Journal and People are top-level alongside the section pages).

```
# Journal database
schema = json.load("databases/journal.json")["schema"]
notion-create-database parent=VAULT_MIRROR_ID title="📔 Journal" properties=schema

# People database
schema = json.load("databases/people.json")["schema"]
notion-create-database parent=VAULT_MIRROR_ID title="👥 People" properties=schema

# Snapchat Contacts database (under Snapchat Intelligence section)
schema = json.load("databases/snapchat-contacts.json")["schema"]
notion-create-database parent=SNAPCHAT_ID title="📸 Snapchat Contacts" properties=schema
```

Record IDs as `JOURNAL_DB_ID`, `PEOPLE_DB_ID`, `SNAP_CONTACTS_DB_ID`.

### 2d. Create default views

```
notion-create-view database_id=JOURNAL_DB_ID type="table" sort=[{property:"Date", direction:"descending"}]
notion-create-view database_id=PEOPLE_DB_ID  type="table" sort=[{property:"Name", direction:"ascending"}]
notion-create-view database_id=SNAP_CONTACTS_DB_ID type="table" sort=[{property:"Name", direction:"ascending"}]
```

---

## Phase 3 — Static pages

For each section folder under `pages/`, read every `.md` file and create a Notion page
under the corresponding section parent.

```
for section, parent_id in [
    ("identity",  IDENTITY_ID),
    ("life",      LIFE_ID),
    ("health",    HEALTH_ID),
    ("interests", INTERESTS_ID),
    ("ai-tech",   AI_TECH_ID),
]:
    files = list(Path(f"pages/{section}").glob("*.md"))
    # Batch 5 at a time to stay under MCP payload limits
    for batch in chunks(files, 5):
        pages = []
        for f in batch:
            text = f.read_text()
            # First line is "# Title" — extract and use as page title
            title_line, body = text.split("\n", 1)
            title = title_line.removeprefix("# ").strip()
            pages.append({"title": title, "content": body.strip()})
        notion-create-pages parent=parent_id pages=pages
```

Expected counts after Phase 3:
- Identity: 10 pages (Core Identity, Close Circle, Roles, + 7 Claude-Brain)
- Life: 7 pages
- Health: 2 pages
- Interests: 2 pages
- AI & Tech: 9 pages

---

## Phase 4 — Database rows

### 4a. Journal database (33 rows)

```
db = json.load("databases/journal.json")
for row in db["rows"]:
    notion-create-pages parent=JOURNAL_DB_ID pages=[{
        properties: {
            Name: row["title"],
            Date: row["properties"]["Date"],
            Type: row["properties"]["Type"],
            Category: row["properties"]["Category"],
            Tags: row["properties"]["Tags"],
            Source: row["properties"]["Source"],
        },
        content: row["content_markdown"],
    }]
```

### 4b. People database (30 rows) — TWO PASS

**Pass 1: create rows without relations.**

```
db = json.load("databases/people.json")
name_to_page_id = {}
for row in db["rows"]:
    response = notion-create-pages parent=PEOPLE_DB_ID pages=[{
        properties: {
            Name: row["title"],
            Type: row["properties"]["Type"],
            Category: row["properties"]["Category"],
            Tags: row["properties"]["Tags"],
            "Date Updated": row["properties"]["Date Updated"],
            Source: row["properties"]["Source"],
        },
        content: row["content_markdown"],
    }]
    name_to_page_id[row["title"]] = response.page_id
```

**Pass 2: wire `Related People` relations.**

```
for row in db["rows"]:
    related_names = row["properties"]["Related People"]
    if not related_names:
        continue
    related_ids = [name_to_page_id[n] for n in related_names if n in name_to_page_id]
    if not related_ids:
        continue
    notion-update-page page_id=name_to_page_id[row["title"]] properties={
        "Related People": related_ids
    }
```

### 4c. Snapchat Contacts database (41 rows)

Same as Journal — single pass, no relations.

```
db = json.load("databases/snapchat-contacts.json")
for row in db["rows"]:
    notion-create-pages parent=SNAP_CONTACTS_DB_ID pages=[{
        properties: {
            Name: row["title"],
            Username: row["properties"]["Username"],
            Era: row["properties"]["Era"],
            Status: row["properties"]["Status"],
            Tags: row["properties"]["Tags"],
        },
        content: row["content_markdown"],
    }]
```

---

## Phase 5 — Snapchat Intelligence pages

Two static pages under `SNAPCHAT_ID`:

```
for fname in ["snapchat/overview.md", "snapchat/notable-threads.md"]:
    text = Path(fname).read_text()
    title_line, body = text.split("\n", 1)
    title = title_line.removeprefix("# ").strip()
    notion-create-pages parent=SNAPCHAT_ID pages=[{
        title: title,
        content: body.strip(),
    }]
```

---

## Phase 6 — Verification

Run these checks; record results in a new `EXECUTION_LOG.md` in this folder:

1. `notion-search query="📖 Vault Mirror"` → returns 1 result
2. `notion-fetch id=JOURNAL_DB_ID` → row count == 33
3. `notion-fetch id=PEOPLE_DB_ID` → row count == 30
4. `notion-fetch id=SNAP_CONTACTS_DB_ID` → row count == 41
5. Spot-check: open Emma Williard in People DB → confirm `Related People` shows
   resolved page links to Trey Frachiseur and Ethan Arce, content body intact
6. Spot-check: open `Core Identity` page → "Deep Profile" section present, no
   `[[wikilinks]]` remaining, no raw YAML
7. Spot-check: open most-recent journal entry → date set correctly, body present

If any check fails, log the failure with the page/row in question and the MCP error
returned. Don't retry blindly — diagnose first.

---

## Phase 7 — Final commit (back in the web session)

After successful execution on Jackson's local machine, the EXECUTION_LOG.md from
Phase 6 should be committed back to the branch. From the web session:

```bash
git pull origin claude/obsidian-to-notion-migration-0E8WD
git add "AI & Tech/migrations/2026-04-13-obsidian-to-notion/EXECUTION_LOG.md"
git commit -m "Migration executed: log Notion writes + verification results"
git push origin claude/obsidian-to-notion-migration-0E8WD
```

---

## Failure handling

- **Rate limits:** Pause 5s between batches if you hit a 429.
- **Payload too large:** Split batches smaller. If a single page body is too large
  (>50KB markdown), create the page first with a short body, then update with the
  full content via `notion-update-page`.
- **Property type mismatch:** The `select`/`multi_select` options are derived from
  observed values. If Notion rejects an unknown option, set the property to `None`
  for that row and log it; don't fail the whole batch.
- **Wikilink resolution gaps:** Pass 2 only wires relations where the target name
  exists in the People DB. Anyone referenced but not present (e.g. someone in
  `related_people:` who doesn't have a People/*.md file) is silently skipped — log
  these for follow-up.
