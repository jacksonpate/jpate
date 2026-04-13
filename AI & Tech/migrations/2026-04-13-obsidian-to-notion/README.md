# Obsidian → Notion Migration Package

**Built:** 2026-04-13
**Source vault:** `/home/user/jpate` (mirror of `C:/Users/jacks/Desktop/Project_P`)
**Target:** Jackson Pate Notion workspace → new `📖 Vault Mirror` root page
**Branch:** `claude/obsidian-to-notion-migration-0E8WD`

---

## Why this is a package, not a live migration

The Notion MCP tools (`mcp__claude_ai_Notion__notion-create-pages`, etc.) are listed in
`.claude/settings.local.json` but those settings reflect the **local Windows Claude
Code setup**. They are NOT exposed in the Claude Code on-the-web environment where this
branch was built.

So instead of writing to Notion directly, this branch produces a **complete, ready-to-import
package**: cleaned markdown for every page, structured JSON for every database row, plus
exact executor instructions (`EXECUTOR.md`). Run the executor from any session that has
the Notion MCP connected — typically NOVA on Jackson's local Windows machine.

---

## What's in the package

```
2026-04-13-obsidian-to-notion/
├── README.md                          ← you are here
├── EXECUTOR.md                        ← step-by-step MCP call sequence for NOVA
├── manifest.json                      ← machine-readable index of everything
│
├── pages/                             ← 30 static pages (cleaned markdown, ready to upload)
│   ├── identity/    (10)              Core + Claude-Brain identity files
│   ├── life/         (7)              Active situations, personal arc, vision, journals
│   ├── health/       (2)              Health protocol, medication & supplements
│   ├── interests/    (2)              Interests Lab, Gear
│   └── ai-tech/      (9)              Dev logs, design specs, scripts index
│
├── databases/                         ← 3 databases (schema + rows in JSON)
│   ├── journal.json                   33 entries
│   ├── people.json                    30 entries (with Related People relations)
│   └── snapchat-contacts.json         41 entries
│
└── snapchat/                          ← Synthesized intelligence pages (not raw dump)
    ├── overview.md                    Relationship map + era analysis + key patterns
    └── notable-threads.md             Top 10 conversations summarized
```

**Totals:** 30 static pages + 3 databases (104 rows) + 2 synthesis pages = full coverage of
the important content from the 495-file vault.

## What was intentionally skipped

| Skipped | Why |
|---|---|
| `agents/` (inboxes, Shared_Log, JOURNAL, STATUS, handoff) | Operational coordination, not personal info |
| `Memory/` standing-rules + feedback files | Agent operating rules, not Jackson's content |
| `Personal Data/Snapchat/Messages/*.md` (raw 304+ files) | Represented via synthesized Notable Threads + Contacts DB |
| Python script source code | Documented on `pages/ai-tech/scripts-index.md`; code stays in the repo |
| `*.base` placeholder files | Empty (39 bytes each) |

---

## Translation rules applied

1. **YAML frontmatter** → rendered as a `## Source Properties` block at the top of each
   page (for static pages), or mapped to Notion properties (for database rows).
2. **`[[Wikilinks]]`** → converted to `**bold text**`. Notion mentions can be wired up in
   a second pass once pages exist (see EXECUTOR.md "Pass 2: Wire relations").
3. **`## Related` sections** that were just lists of wikilinks → dropped (Notion handles
   backlinks automatically through mentions).
4. **`## Mentioned In` sections** with rich narrative content → preserved as-is.

## How to execute

Open `EXECUTOR.md` and follow the phases. The package is self-contained — no need to
re-read the source vault during execution. Every page is a standalone markdown file
ready to drop into a `notion-create-pages` call.

## How to rebuild

If the vault changes and the package needs regenerating:

```bash
cd /home/user/jpate
python3 "AI & Tech/scripts/build_notion_migration.py"
```

The script is idempotent — it overwrites the package folder. Source files are never
modified.
