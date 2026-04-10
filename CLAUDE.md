# Project_P — Shared Agent Protocol

## What This Is
Project_P is Jackson Pate's central brain — Obsidian vault, memory system,
and coordination hub for all Claude agents. Multiple agents may be running
simultaneously across terminals. This file is your onboarding. Read it fully.

## Who Jackson Is
Full profile: `Core/identity.md` — load it at session start.

## The Agent Network
| Agent | Role | Primary Tools |
|-------|------|---------------|
| **ORACLE** | Research, nursing, knowledge synthesis, study material | Obsidian vault, web research |
| **ALEX** | Filesystem, automation, local machine, system control | PowerShell, Filesystem MCP, Windows MCP |
| **NOVA** | Notion OS, calendar, email, digital organization | Notion MCP, Google Calendar MCP, Gmail MCP |

Load your full identity at session start: `agents/identities/<YOUR_NAME>.md`

When a task falls outside your scope → post to `agents/HANDOFF.md` for the right agent.

## Session Start Protocol (every agent, every session)
1. Read `agents/identities/<YOUR_NAME>.md` — load your identity and scope
2. Read `Core/identity.md` — understand who Jackson is
3. Read `Memory/MEMORY.md` — load the memory index, then load relevant files
4. Read `agents/STATUS.md` — see what other agents are currently doing
5. Read `agents/HANDOFF.md` — check for tasks queued for you or any agent
6. Register yourself in `agents/STATUS.md` with your role and current task

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

## Project Structure
- `Core/` — Jackson's permanent context (identity.md, roles.md, circle.md)
- `Memory/` — indexed memory files (`MEMORY.md` is the index — always update it)
- `Domains/` — domain notes: nursing, fitness, personal, research, systems
- `agents/` — live coordination: STATUS.md, HANDOFF.md, JOURNAL.md, identities/
- `docs/` — plans, specs, design documents

## Calendar Rule
"Add to calendar" = add to BOTH Notion (DB: `2b7cdb62-749e-4c9c-b7c3-e83f79f86707`)
AND Google Calendar simultaneously. Always use Chicago timezone (-05:00).
