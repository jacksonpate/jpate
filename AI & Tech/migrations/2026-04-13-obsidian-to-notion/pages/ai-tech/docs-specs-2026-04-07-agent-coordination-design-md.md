# 2026 04 07 Agent Coordination Design

*Source: AI & Tech/docs/specs/2026-04-07-agent-coordination-design.md*

# Agent Coordination System — Design Spec
**Date:** 2026-04-07  
**Project:** Project_P  
**Status:** Approved

---

## Problem

Multiple Claude Code instances run simultaneously across terminals. Each is
isolated — they share no memory or runtime state. Without coordination, agents
duplicate work, overwrite each other's files, and Jackson has to manually
context-switch between them.

## Goal

Make all agents feel like one unified system: shared awareness, task handoff,
help requests, and full PC autonomy — all through the filesystem.

---

## Architecture

The filesystem is the shared medium. Every agent reads `CLAUDE.md` at session
start. Three coordination files in `agents/` handle live state.

```
Project_P/
├── CLAUDE.md              ← loaded by every agent, onboarding + protocol
├── agents/
│   ├── STATUS.md          ← who's active and what they're doing right now
│   ├── HANDOFF.md         ← task queue: requests, pickups, handoffs
│   └── JOURNAL.md         ← append-only log of completed work
├── Core/                  ← identity, roles, circle
├── Memory/                ← indexed memory files
├── Domains/               ← domain notes (nursing, fitness, personal, etc.)
└── docs/                  ← plans, specs, design documents
```

---

## CLAUDE.md (Project_P root)

Loaded automatically by every Claude session opened in this directory.

```markdown
# Project_P — Shared Agent Protocol

## What This Is
Project_P is Jackson Pate's central brain — Obsidian vault, memory system,
and coordination hub for all Claude agents. Multiple agents may be running
simultaneously across terminals. This file is your onboarding.

## Session Start Protocol (every agent, every session)
1. Read `Core/identity.md` — understand who Jackson is
2. Read `Memory/MEMORY.md` — load the memory index
3. Read `agents/STATUS.md` — see what other agents are currently doing
4. Read `agents/HANDOFF.md` — check for tasks queued for you or any agent
5. Register yourself in `agents/STATUS.md` with your role and current task

## Session End / Checkpoint Protocol
1. Update your entry in `agents/STATUS.md` with progress, or remove it if done
2. If handing work off → add an item to `agents/HANDOFF.md`
3. If completing significant work → append an entry to `agents/JOURNAL.md`
4. If you discovered something worth remembering → write to `Memory/`

## Coordination Rules
- Before starting any task, check STATUS.md to avoid duplicating active work
- Before writing to any Core/ or Memory/ file, check if another agent owns it
- Claim tasks in HANDOFF.md by writing your name in "Claimed by" before starting
- Never leave STATUS.md stale — update or remove your entry when done

## Available Tools (MCP Servers + System Access)

| Tool | What it does |
|------|-------------|
| **Filesystem MCP** | Read/write any file on Jackson's PC |
| **Windows MCP** | Windows system interactions |
| **Bash (PowerShell)** | Run ANY system command — volume, apps, processes, registry, etc. |
| **Playwright MCP** | Control browsers and web apps visually |
| **Notion MCP** | Read/write Jackson's Notion workspace |
| **Google Calendar MCP** | View and create calendar events |
| **Gmail MCP** | Read/draft/search email |

### System Control via PowerShell (Bash tool)
- Volume: `nircmd` or `Set-Volume`
- Launch apps: `Start-Process "spotify"`
- Kill processes: `Stop-Process -Name "..."`
- Spotify control: Spotify Web API or SendKeys for play/pause/skip
- Window management: Win32 API via `Add-Type`

Agents should never ask Jackson to manually do something a PowerShell
command or MCP server can handle. Full autonomy is the goal.

## Project Structure
- `Core/` — Jackson's permanent identity context (identity.md, roles.md, circle.md)
- `Memory/` — indexed memory files (MEMORY.md is the index — always update it)
- `Domains/` — domain notes: nursing, fitness, personal, research, etc.
- `agents/` — live coordination between active Claude sessions
- `docs/` — plans, specs, and design documents
```

---

## agents/STATUS.md

Live snapshot. Every agent registers on start, updates on progress, removes
entry or moves to Idle on completion.

```markdown
# Agent Status

Last updated: YYYY-MM-DD

## Active Agents

### Agent: [Role/Name]
- **Task:** [What you're doing right now]
- **Working in:** [Which files/directories]
- **Status:** In progress
- **Started:** YYYY-MM-DD
- **Notes:** [Anything other agents need to know — files to avoid, etc.]

## Idle / Completed Agents
<!-- Move entries here when done, or delete -->
```

---

## agents/HANDOFF.md

Task queue. Agents post work here when they finish something that needs a
follow-up, or when they're stuck and need another agent to pick it up.

```markdown
# Handoff Queue

## Pending

### [HIGH/MED/LOW] Task title
- **From:** [Agent role that posted this]
- **For:** [Specific agent role, or "Any agent"]
- **Context:** [What was done, what's needed next, relevant file paths]
- **Claimed by:** _(unclaimed)_

## Completed
<!-- Move items here after finishing, with date -->
```

---

## agents/JOURNAL.md

Append-only log. Written to when significant work is completed. Gives future
agents (and Jackson) a running history of what happened and why.

```markdown
# Agent Journal

## YYYY-MM-DD

### [Agent Role]
- What was done
- What was produced (file paths, memory entries, etc.)
- Decisions made and why
- Handed off: [task] to [agent/queue]
```

---

## Agent Behavior Protocol

### On Session Start
1. Read `CLAUDE.md` (automatic)
2. Read `Core/identity.md`
3. Read `Memory/MEMORY.md`
4. Read `agents/STATUS.md` — understand active agents, avoid conflicts
5. Read `agents/HANDOFF.md` — claim any relevant pending tasks
6. Write your entry into `agents/STATUS.md`

### During Work
- Update `STATUS.md` at meaningful checkpoints
- Check `HANDOFF.md` if work scope expands unexpectedly
- Use Filesystem MCP, PowerShell, Playwright freely — full autonomy

### On Session End
- Update `STATUS.md` (mark done or remove entry)
- Post to `HANDOFF.md` if follow-up work is needed
- Append to `JOURNAL.md` if significant work was completed
- Write new memory files if anything important was learned

---

## What This Solves

| Problem | Solution |
|---------|----------|
| Agents duplicate work | STATUS.md — check before starting |
| Agents overwrite each other | STATUS.md — claim files/dirs |
| Work gets lost between sessions | JOURNAL.md — persistent history |
| Can't hand off tasks | HANDOFF.md — structured queue |
| Agents need Jackson for system tasks | PowerShell + MCPs — full autonomy |
| Agents don't know who Jackson is | CLAUDE.md → Core/identity.md |
