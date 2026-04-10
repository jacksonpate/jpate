# Notion → Obsidian Migration Design Spec
**Date:** 2026-04-07
**Status:** Approved

---

## Overview

Fetch all meaningful content from Jackson's Notion workspace and write it into the Obsidian vault at `Project_P`, organized using the existing ring model. Notion is kept intact — this is a read-only copy operation. Notion links in migrated content are converted to plain text (no dead links).

---

## Source: Notion Workspace Structure

```
Jackson Pate (root)
├── Academic Hub                        ← classes, assignments, Auburn
├── Task Manager                        ← SKIP (operational)
├── Health Protocol                     ← training, recovery, nutrition
│   ├── Physical health notes
│   └── (subpages)
├── Mind Vault                          ← most content-rich section
│   ├── Thought Journal                 ← personal journal Sept 2025–Mar 2026
│   ├── Notability Inbox                ← SKIP (inbox/operational)
│   └── Academic Integrity Defense      ← Spring 2026 defense document
├── Interests Lab                       ← AI, philosophy, markets
├── Backstage / Links                   ← SKIP (navigation wrappers)
└── Ultimate ADHD Brain 2.0
    ├── Mental Health → Journals DB     ← migrate as individual entries
    ├── Goals DB                        ← migrate as individual entries
    ├── Organize / Projects / Routines  ← SKIP (empty or operational)
    ├── Areas / Brain Dumps / Notes     ← SKIP (empty templates)
    └── Archive                         ← fetch page + all subpages; migrate any with real content
```

---

## Target: Obsidian Vault Structure

```
Core/
  identity.md          ← UPDATED: merge Mind Vault "Who I Am" section in
  circle.md            ← NEW: close circle, relationships, romantic history

Domains/personal/
  active-situations.md ← Mind Vault "Active Situations" section
  personal-arc.md      ← "Personal arc — Sept 2025 to April 2026" page
  long-term-vision.md  ← "Long-term vision" page
  journal/             ← Thought Journal (1 .md file per dated entry)
    2025-09-27-1.md
    2025-09-28-1.md
    2025-10-27-1.md    ← duplicate dates get -N suffix
    2025-10-27-2.md
    ... (one per entry)
  journals/            ← Mental Health Journals database (1 .md per entry)
    YYYY-MM-DD-<title>.md
  goals/               ← Goals database (1 .md per goal)
    <goal-name>.md

Domains/nursing/
  academic-hub.md             ← Academic Hub page content
  academic-integrity-defense.md

Domains/fitness/
  health-protocol.md
  medication-supplement-protocol.md
  physical-health-notes.md

Domains/ai-research/
  interests-lab.md
```

---

## Migration Rules

### Content Conversion
- Strip Notion navigation chrome (the repeated sidebar links present on every page)
- Strip callout wrappers that are purely structural (e.g., "Add New" action buttons)
- Convert Notion page links to plain text: `[Page Title](notion url)` → `Page Title`
- Preserve all actual content: headings, lists, callouts with real text, tables, dates
- Preserve emojis in headings where they carry meaning

### Core/identity.md Update
- Read existing `Core/identity.md`
- Append Mind Vault "Who I Am" section as a new `## Deep Profile` heading
- Do not overwrite the existing content — merge only

### Core/circle.md (new)
- Source: Mind Vault "Close Circle" and "Romantic history" sections
- Include: roommates, closest friends, family, romantic history

### Database Export (one note per entry)
- **Journals DB**: Each journal entry → `Domains/personal/journals/YYYY-MM-DD-<title>.md`
  - Frontmatter: `date`, `title`, `type`
- **Goals DB**: Each goal → `Domains/personal/goals/<goal-name>.md`
  - Frontmatter: `title`, `status` (if available)
- **Thought Journal**: Already one page with multiple dated sections — split into individual files under `Domains/personal/journal/`, numbered and dated

### What to Skip
- Empty template pages (no body content beyond the template callout)
- Operational/task management pages (Task Manager, Organize)
- Navigation wrapper pages (Backstage, Links, Dispatch Table)
- Tutorial pages (How Everything Works, Using the Daily Home Page)
- Notability Inbox (operational capture inbox)

---

## Execution Order

1. Fetch and inspect pages that haven't been fully read yet (Academic Hub, Health Protocol subpages, Interests Lab, Goals DB, Journals DB, Personal arc, Long-term vision, Archive)
2. Update `Core/identity.md` with Mind Vault "Who I Am"
3. Create `Core/circle.md`
4. Create `Domains/personal/` files (active-situations, personal-arc, long-term-vision)
5. Split and create Thought Journal individual entries
6. Export Journals database entries
7. Export Goals database entries
8. Create `Domains/nursing/` files
9. Create `Domains/fitness/` files
10. Create `Domains/ai-research/interests-lab.md`

---

## Success Criteria

- Every page with real content has a corresponding `.md` file in the vault
- No Notion navigation chrome in any migrated file
- No dead Notion links — all converted to plain text
- `Core/identity.md` contains the merged deep profile
- Database entries are individual files with frontmatter
- Obsidian graph view shows meaningful connections across Domains
