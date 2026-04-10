# Agent Coordination System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a filesystem-based coordination system so all Claude agents running in Project_P terminals share awareness, hand off tasks, and operate with full PC autonomy.

**Architecture:** Every agent reads `CLAUDE.md` at session start — this is the shared protocol. Three files in `agents/` handle live state: STATUS.md (who's doing what), HANDOFF.md (task queue), JOURNAL.md (history). No code — purely markdown files and conventions.

**Tech Stack:** Markdown files, Claude Code CLAUDE.md auto-loading

---

### Task 1: Create the `agents/` directory and STATUS.md

**Files:**
- Create: `C:/Users/jacks/Project_P/agents/STATUS.md`

- [ ] **Step 1: Create the agents directory and STATUS.md**

Create `C:/Users/jacks/Project_P/agents/STATUS.md` with this exact content:

```markdown
# Agent Status

Last updated: 2026-04-07

## Active Agents

<!-- Each agent registers here on session start. Format:

### Agent: [Role/Name]
- **Task:** [What you're doing right now]
- **Working in:** [Which files/directories you're actively modifying]
- **Status:** In progress
- **Started:** YYYY-MM-DD
- **Notes:** [Anything other agents need to know — files to avoid, conflicts, etc.]

Remove or move your entry to "Idle" when done. -->

## Idle / Completed Agents

<!-- Move entries here when done, or delete them entirely -->
```

- [ ] **Step 2: Verify the file exists and is readable**

Run:
```bash
cat "C:/Users/jacks/Project_P/agents/STATUS.md"
```
Expected: Full file contents print without error.

- [ ] **Step 3: Commit**

```bash
git -C "C:/Users/jacks/Project_P" add agents/STATUS.md
git -C "C:/Users/jacks/Project_P" commit -m "feat: add agent STATUS.md coordination file"
```

---

### Task 2: Create `agents/HANDOFF.md`

**Files:**
- Create: `C:/Users/jacks/Project_P/agents/HANDOFF.md`

- [ ] **Step 1: Create HANDOFF.md**

Create `C:/Users/jacks/Project_P/agents/HANDOFF.md` with this exact content:

```markdown
# Handoff Queue

Tasks posted here by one agent for another to pick up. Check this at session
start. Claim a task by writing your agent name in "Claimed by" before starting.

## Pending

<!-- Format:
### [HIGH/MED/LOW] Task title
- **From:** [Agent role that posted this]
- **For:** [Specific agent role, or "Any agent"]
- **Context:** [What was done, what's needed next, relevant file paths]
- **Claimed by:** _(unclaimed)_
-->

## Completed

<!-- Move items here after finishing. Include the date completed. -->
```

- [ ] **Step 2: Verify**

Run:
```bash
cat "C:/Users/jacks/Project_P/agents/HANDOFF.md"
```
Expected: Full file contents print without error.

- [ ] **Step 3: Commit**

```bash
git -C "C:/Users/jacks/Project_P" add agents/HANDOFF.md
git -C "C:/Users/jacks/Project_P" commit -m "feat: add agent HANDOFF.md task queue"
```

---

### Task 3: Create `agents/JOURNAL.md`

**Files:**
- Create: `C:/Users/jacks/Project_P/agents/JOURNAL.md`

- [ ] **Step 1: Create JOURNAL.md**

Create `C:/Users/jacks/Project_P/agents/JOURNAL.md` with this exact content:

```markdown
# Agent Journal

Append-only log. Add an entry whenever you complete significant work.
Never delete or edit past entries — only append.

## Format

### YYYY-MM-DD — [Agent Role]
- **Done:** What was completed
- **Produced:** File paths, memory entries, Notion pages, etc.
- **Decisions:** Any choices made and why
- **Handed off:** What was posted to HANDOFF.md (if anything)

---

## Log

<!-- Entries go here, newest at the top -->
```

- [ ] **Step 2: Verify**

Run:
```bash
cat "C:/Users/jacks/Project_P/agents/JOURNAL.md"
```
Expected: Full file contents print without error.

- [ ] **Step 3: Commit**

```bash
git -C "C:/Users/jacks/Project_P" add agents/JOURNAL.md
git -C "C:/Users/jacks/Project_P" commit -m "feat: add agent JOURNAL.md history log"
```

---

### Task 4: Create `CLAUDE.md` in Project_P root

This is the most important file — loaded automatically by every Claude session
opened in this directory.

**Files:**
- Create: `C:/Users/jacks/Project_P/CLAUDE.md`

- [ ] **Step 1: Create CLAUDE.md**

Create `C:/Users/jacks/Project_P/CLAUDE.md` with this exact content:

```markdown
# Project_P — Shared Agent Protocol

## What This Is
Project_P is Jackson Pate's central brain — Obsidian vault, memory system,
and coordination hub for all Claude agents. Multiple agents may be running
simultaneously across terminals. This file is your onboarding. Read it fully.

## Who Jackson Is
- 20yo nursing student at Auburn University. Long-term goal: PMHNP.
- Systems thinker. Learning to code. Deep into AI and automation daily.
- Direct and structured — no fluff. Deep understanding over surface answers.
- Timezone: Chicago (UTC-05:00)
- Full profile: `Core/identity.md`

## Session Start Protocol (every agent, every session)
1. Read `Core/identity.md` — understand who Jackson is before anything else
2. Read `Memory/MEMORY.md` — load the memory index, then load relevant files
3. Read `agents/STATUS.md` — see what other agents are currently doing
4. Read `agents/HANDOFF.md` — check for tasks queued for you or any agent
5. Register yourself in `agents/STATUS.md` with your role and current task

## Session End / Checkpoint Protocol
1. Update your entry in `agents/STATUS.md` — progress note, or remove if done
2. If handing work off → add an item to `agents/HANDOFF.md`
3. If completing significant work → append an entry to `agents/JOURNAL.md`
4. If you learned something worth remembering → write a memory file to `Memory/`
   and update `Memory/MEMORY.md` index

## Coordination Rules
- Check `agents/STATUS.md` before starting any task — avoid duplicating work
- Before writing to any `Core/` or `Memory/` file, check if another agent owns it
- Claim tasks in `HANDOFF.md` by writing your name before starting
- Never leave `STATUS.md` stale — update or remove your entry when done
- If you're stuck on something another agent could help with → post to HANDOFF.md

## Available Tools (use freely — full autonomy)

| Tool | What it does |
|------|-------------|
| **Filesystem MCP** | Read/write any file on Jackson's PC |
| **Windows MCP** | Windows system interactions |
| **Bash (PowerShell)** | ANY system command — volume, apps, processes, registry |
| **Playwright MCP** | Control browsers and web apps visually |
| **Notion MCP** | Read/write Jackson's Notion workspace |
| **Google Calendar MCP** | View and create calendar events (Chicago timezone -05:00) |
| **Gmail MCP** | Read/draft/search email |

### System Control via PowerShell (Bash tool)
- Volume up/down: `(New-Object -ComObject WScript.Shell).SendKeys([char]175)`
- Mute: `(New-Object -ComObject WScript.Shell).SendKeys([char]173)`
- Launch Spotify: `Start-Process "spotify"`
- Play/Pause Spotify: `(New-Object -ComObject WScript.Shell).SendKeys([char]179)`
- Next track: `(New-Object -ComObject WScript.Shell).SendKeys([char]176)`
- Kill a process: `Stop-Process -Name "processname" -Force`
- Open a URL: `Start-Process "https://example.com"`
- List running processes: `Get-Process | Sort-Object CPU -Descending | Select-Object -First 20`

Never ask Jackson to manually do something a PowerShell command or MCP can handle.

## Project Structure
- `Core/` — Jackson's permanent context (identity.md, roles.md, circle.md)
- `Memory/` — indexed memory files (`MEMORY.md` is the index — always update it)
- `Domains/` — domain notes: nursing, fitness, personal, research, systems
- `agents/` — live coordination: STATUS.md, HANDOFF.md, JOURNAL.md
- `docs/` — plans, specs, design documents

## Calendar Rule
"Add to calendar" = add to BOTH Notion (DB: `2b7cdb62-749e-4c9c-b7c3-e83f79f86707`)
AND Google Calendar simultaneously. Always use Chicago timezone (-05:00).
```

- [ ] **Step 2: Verify the file is in the right place**

Run:
```bash
ls "C:/Users/jacks/Project_P/CLAUDE.md"
```
Expected: File listed. Claude Code will now auto-load this for every session opened in Project_P.

- [ ] **Step 3: Commit**

```bash
git -C "C:/Users/jacks/Project_P" add CLAUDE.md
git -C "C:/Users/jacks/Project_P" commit -m "feat: add local CLAUDE.md shared agent protocol"
```

---

### Task 5: Register the currently active agent in STATUS.md

The Notability migration agent is already running. Register it so future agents
know not to conflict with it.

**Files:**
- Modify: `C:/Users/jacks/Project_P/agents/STATUS.md`

- [ ] **Step 1: Add the active agent entry**

Edit `agents/STATUS.md` — replace the `## Active Agents` comment block with:

```markdown
## Active Agents

### Agent: Notability Migration
- **Task:** Migrating Notability notes into Obsidian vault (Project_P)
- **Working in:** `Project_P/Domains/`, `Project_P/Memory/`
- **Status:** In progress
- **Started:** 2026-04-07
- **Notes:** Do not write to Domains/ files without checking here first.
  This agent is actively creating and modifying domain note files.
```

- [ ] **Step 2: Verify**

Run:
```bash
cat "C:/Users/jacks/Project_P/agents/STATUS.md"
```
Expected: Active agent entry for Notability Migration is visible.

- [ ] **Step 3: Commit**

```bash
git -C "C:/Users/jacks/Project_P" add agents/STATUS.md
git -C "C:/Users/jacks/Project_P" commit -m "chore: register active Notability migration agent in STATUS.md"
```

---

### Task 6: Smoke test — simulate a new agent session start

Verify the system works end-to-end by doing exactly what a new agent would do.

- [ ] **Step 1: Read CLAUDE.md as a new agent would**

Run:
```bash
cat "C:/Users/jacks/Project_P/CLAUDE.md"
```
Expected: Full protocol prints. Confirms auto-load will work for any new terminal opened in Project_P.

- [ ] **Step 2: Read STATUS.md**

Run:
```bash
cat "C:/Users/jacks/Project_P/agents/STATUS.md"
```
Expected: Notability Migration agent entry is visible with working in / notes.

- [ ] **Step 3: Read HANDOFF.md**

Run:
```bash
cat "C:/Users/jacks/Project_P/agents/HANDOFF.md"
```
Expected: Empty pending queue — no tasks yet.

- [ ] **Step 4: Confirm all files exist**

Run:
```bash
ls "C:/Users/jacks/Project_P/agents/"
```
Expected: `HANDOFF.md  JOURNAL.md  STATUS.md`

- [ ] **Step 5: Final commit**

```bash
git -C "C:/Users/jacks/Project_P" add -A
git -C "C:/Users/jacks/Project_P" commit -m "feat: agent coordination system complete"
```
