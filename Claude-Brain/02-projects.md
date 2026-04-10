# Active Projects

## jpate — Personal AI Supersystem
- **Repo:** github.com/jacksonpate/jpate
- **Status:** 🟡 In Progress
- **What it is:** Personal AI OS — Claude with full context on Jackson, three agents working together, Obsidian brain (Project_P), Notion as human note layer, everything accessible from anywhere (home PC, iPad, wherever)
- **Architecture:**
  - Obsidian (Project_P) = AI-facing memory / computer's brain
  - Notion = human notes, school, journals, thoughts
  - GitHub = code and project files
  - Claude Code = primary AI interface with 3 agents ([[ORACLE]], [[ALEX]], [[NOVA]])
  - MCP servers: Windows, Filesystem, Notion, Google Calendar, Gmail, Obsidian
- **Agents:**
  - **[[ORACLE]]** — research, nursing, knowledge synthesis
  - **[[ALEX]]** — filesystem, automation, local machine, system control
  - **[[NOVA]]** — Notion OS, calendar, email, digital organization
- **Session hooks:** `session-start.sh` loads brain on every Claude Code session; `end-of-session.sh` logs and commits work
- **Next steps:**
  - [x] Wire session-start hook with absolute paths
  - [x] Push hooks and settings to GitHub
  - [x] Fill in all Claude-Brain files
  - [x] Build and wire Obsidian Local REST API MCP (2026-04-07)
  - [x] Full system diagnosis — 16/16 checks passing (2026-04-07)
  - [ ] Wire Notion API for notes sync (sync-to-notion.py) — fix NOTION_TOKEN in .env
  - [ ] Set up `notes/inbox/` routing to Notion DBs
  - [ ] Make supersystem accessible from iPad / other machines

## Notion Triage Agent
- **Repo:** github.com/jacksonpate/jpate (`agent/` directory)
- **Status:** 🟡 In Progress
- **What it is:** Python agent that monitors a Notion inbox and routes items to the correct DB (school notes, journal, tasks, etc.) automatically
- **Spec:** `docs/superpowers/specs/2026-04-06-notion-triage-agent-design.md`
- **Plan:** `docs/superpowers/plans/2026-04-06-notion-triage-agent.md`
- **Next steps:**
  - [ ] Test classifier against live inbox items
  - [ ] Finalize handler logic for each route
  - [ ] Deploy scheduler (setup_scheduler.ps1)

## Related
- [[06-systems]]
- [[03-goals]]
- [[interests-lab]]
- [[ORACLE]]
- [[ALEX]]
- [[NOVA]]
- [[ANI]]
