# Obsidian Brain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `Project_P` into a shared Obsidian vault that is the single source of truth for both Jackson's identity/notes and Claude's memory.

**Architecture:** Ring model — `Core/` holds Jackson's identity (nucleus), `Memory/` holds Claude's structured memory files, `Domains/` holds notes by life area. Claude has full read/write access to all three. CLAUDE.md is updated to redirect Claude's session-start reads and all memory writes to this vault.

**Tech Stack:** Markdown files, Obsidian (local vault), Claude's file tools (Read/Write/Edit)

---

### Task 1: Create vault folder structure

**Files:**
- Create: `Core/` (directory)
- Create: `Memory/` (directory)
- Create: `Domains/nursing/`, `Domains/fitness/`, `Domains/ai-research/`, `Domains/finances/` (directories)

- [ ] **Step 1: Create Core and Memory directories**

```bash
mkdir -p "C:/Users/jacks/Project_P/Core"
mkdir -p "C:/Users/jacks/Project_P/Memory"
```

- [ ] **Step 2: Create Domains subdirectories**

```bash
mkdir -p "C:/Users/jacks/Project_P/Domains/nursing"
mkdir -p "C:/Users/jacks/Project_P/Domains/fitness"
mkdir -p "C:/Users/jacks/Project_P/Domains/ai-research"
mkdir -p "C:/Users/jacks/Project_P/Domains/finances"
```

- [ ] **Step 3: Verify structure**

```bash
ls -R "C:/Users/jacks/Project_P/" | grep -v docs | grep -v .obsidian
```

Expected output shows: `Core/`, `Memory/`, `Domains/nursing`, `Domains/fitness`, `Domains/ai-research`, `Domains/finances`

---

### Task 2: Create Core/identity.md

**Files:**
- Create: `Core/identity.md`

- [ ] **Step 1: Write identity.md**

Create `Core/identity.md` with the following content:

```markdown
# Jackson Pate — Identity

## Who I Am
- 20 years old
- Nursing student at Auburn University
- Long-term goal: PMHNP (Psychiatric-Mental Health Nurse Practitioner)
- Timezone: Chicago (UTC-05:00)

## How I Think
- Systems thinker — I see patterns, workflows, and structure in everything
- Learning to code, deep into AI and automation daily
- Prefer direct, structured communication — no fluff

## What Drives Me
- Building systems that actually work and scale
- Merging healthcare with AI and technology
- Understanding things deeply, not just surface-level

## Communication Style
- Direct and structured
- No pleasantries or narration
- Deep understanding over surface answers
- One clarifying question max when needed
```

- [ ] **Step 2: Verify file exists and has content**

Read `Core/identity.md` and confirm it is populated correctly.

---

### Task 3: Create Core/roles.md

**Files:**
- Create: `Core/roles.md`

- [ ] **Step 1: Write roles.md**

Create `Core/roles.md` with the following content:

```markdown
# Jackson's Roles

Claude identifies the active role on every request and operates from it.

| Role | Domain |
|------|--------|
| 🎓 Nursing Student | Nursing concepts, exams, clinicals, pharmacology |
| 🧠 Study Architect | Study systems, schedules, guides, spaced repetition |
| 📋 Life Planner | Goals, decisions, career path, finances |
| 🪞 Reflective Partner | Feelings, relationships, personal processing |
| 💪 Health & Fitness Coach | Gym, supplements, diet, recovery, programming |
| 🔬 Research Analyst | AI in healthcare, deep research, synthesis |
| ⚙️ Systems Architect | Notion, workflows, automation, tech infrastructure |

## How to Use Roles
- Identify the role that fits the request
- If a Skill SOP exists for the task, follow it
- Multiple roles can be active simultaneously (e.g., Research Analyst + Nursing Student)
```

- [ ] **Step 2: Verify file exists and has content**

Read `Core/roles.md` and confirm it is populated correctly.

---

### Task 4: Create Memory/MEMORY.md index

**Files:**
- Create: `Memory/MEMORY.md`

- [ ] **Step 1: Write MEMORY.md**

Create `Memory/MEMORY.md` with the following content:

```markdown
# Memory Index

This file is Claude's memory index for the Obsidian Brain vault.
Read this at the start of every session, then load relevant memory files from this directory.

## Memory Files

<!-- Memory entries will be added here as they are created -->
<!-- Format: - [Title](filename.md) — one-line hook -->
```

- [ ] **Step 2: Verify file exists**

Read `Memory/MEMORY.md` and confirm it is correct.

---

### Task 5: Update global CLAUDE.md

**Files:**
- Modify: `C:/Users/jacks/.claude/CLAUDE.md`

This is the most critical step — it redirects Claude's behavior for all future sessions.

- [ ] **Step 1: Read current CLAUDE.md**

Read `C:/Users/jacks/.claude/CLAUDE.md` in full to understand its current structure before editing.

- [ ] **Step 2: Add Obsidian Brain section**

Add the following section to `CLAUDE.md` directly after the `## Active MCP Servers` section:

```markdown
## Obsidian Brain — Memory System

`Project_P` (`C:\Users\jacks\Project_P`) is the single source of truth for all memory.

**Session start protocol (every session):**
1. Read `C:\Users\jacks\Project_P\Core\identity.md` — understand who Jackson is before anything else
2. Read `C:\Users\jacks\Project_P\Memory\MEMORY.md` — load the memory index
3. Load any memory files from the index that are relevant to the current conversation

**Writing memory:**
- All new memory files go to `C:\Users\jacks\Project_P\Memory\`
- Update `C:\Users\jacks\Project_P\Memory\MEMORY.md` index whenever a new memory file is created
- Do NOT write memory to the `.claude` projects folder

**Writing notes:**
- Claude may add to or update any file in `C:\Users\jacks\Project_P\Core\` or `C:\Users\jacks\Project_P\Domains\`
- Update `Core\identity.md` when new identity-relevant information surfaces
- Add domain notes to `Domains\<area>\` when relevant (nursing concepts, research, fitness, etc.)
```

- [ ] **Step 3: Verify the edit**

Read `C:/Users/jacks/.claude/CLAUDE.md` and confirm the new section is present and correctly placed.

---

### Task 6: Verify end-to-end setup

- [ ] **Step 1: Verify full vault structure**

```bash
find "C:/Users/jacks/Project_P" -not -path "*/docs/*" -not -path "*/.git/*" | sort
```

Expected output includes:
```
Project_P/Core/identity.md
Project_P/Core/roles.md
Project_P/Memory/MEMORY.md
Project_P/Domains/nursing
Project_P/Domains/fitness
Project_P/Domains/ai-research
Project_P/Domains/finances
```

- [ ] **Step 2: Open vault in Obsidian**

In Obsidian: Open Vault → navigate to `C:\Users\jacks\Project_P` → Open.

Confirm:
- `Core`, `Memory`, `Domains` appear in the file explorer
- Graph view shows `identity.md` and `roles.md` as nodes
- No errors on open

- [ ] **Step 3: Confirm CLAUDE.md is updated**

Start a new Claude Code session in `Project_P`. Claude should reference Jackson's identity from `Core/identity.md` without being asked.

- [ ] **Step 4: Test Claude writing memory**

Ask Claude to save a memory. Confirm the file appears in `C:\Users\jacks\Project_P\Memory\` and is visible in Obsidian.
