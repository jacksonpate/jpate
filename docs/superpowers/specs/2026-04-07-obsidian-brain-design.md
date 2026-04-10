# Obsidian Brain — Design Spec
**Date:** 2026-04-07
**Status:** Approved

---

## Overview

`Project_P` serves as both the Obsidian vault root and Claude's working directory. It is a shared, persistent brain — Jackson's identity, notes, and domain knowledge live alongside Claude's structured memory. Claude has full read/write access to the entire vault.

---

## Vault Structure

```
Project_P/
├── .obsidian/              ← Obsidian app config (auto-generated on first open)
├── Core/                   ← Jackson's identity — the nucleus
│   ├── identity.md         ← Who he is: background, values, goals, context
│   └── roles.md            ← The 7 roles and what each means
├── Memory/                 ← Claude's structured memory
│   ├── MEMORY.md           ← Index Claude reads first every session
│   ├── user_*.md           ← User profile memories
│   ├── feedback_*.md       ← Behavioral feedback memories
│   ├── project_*.md        ← Project/initiative memories
│   └── reference_*.md      ← External resource pointers
└── Domains/                ← Notes by life area (both Jackson and Claude contribute)
    ├── nursing/
    ├── fitness/
    ├── ai-research/
    └── finances/
```

---

## Claude's Behavior

### Session Start
1. Read `Core/identity.md` — build context on who Jackson is before anything else
2. Read `Memory/MEMORY.md` — load the memory index and relevant memory files

### During Session
- Write new memory entries to `Memory/` (same frontmatter format as current system)
- Update `Core/identity.md` or `Core/roles.md` when new identity-relevant information surfaces
- Add or update notes in `Domains/` when relevant (nursing concepts, research findings, fitness logs, etc.)

### Memory File Format
Memory files continue to use the existing frontmatter format:
```markdown
---
name: {{memory name}}
description: {{one-line description}}
type: {{user | feedback | project | reference}}
---

{{content}}
```

---

## CLAUDE.md Changes Required

Two updates to the global `~/.claude/CLAUDE.md`:

1. **Memory path** — instruct Claude to read/write memory from `C:\Users\jacks\Project_P\Memory\` instead of the `.claude` projects memory folder
2. **Session start** — instruct Claude to read `C:\Users\jacks\Project_P\Core\identity.md` at the start of every session

---

## Migration

Move existing memory files from:
```
C:\Users\jacks\.claude\projects\C--Users-jacks-Project_P\memory\
```
To:
```
C:\Users\jacks\Project_P\Memory\
```

---

## Ownership Model

| Area | Jackson | Claude |
|------|---------|--------|
| `Core/` | Primary author | Can update when new identity info surfaces |
| `Memory/` | Can read | Primary author |
| `Domains/` | Primary author | Can add/update notes as collaborator |

---

## Success Criteria

- Opening `Project_P` in Obsidian shows the full brain with graph view working
- Claude reads `Core/identity.md` every session without being asked
- Claude writes memory to `Memory/` and it appears in Obsidian immediately
- Domain notes added by Claude are visible and editable in Obsidian
- No memory lives in the `.claude` folder — `Project_P` is the single source of truth
