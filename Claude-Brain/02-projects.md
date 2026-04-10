# Active Projects

## jpate — Personal AI Supersystem
- **Repo:** github.com/jacksonpate/jpate
- **Status:** 🟢 Operational
- **What it is:** Personal AI OS — Claude with full context on Jackson, three agents working together, Obsidian brain (Project_P), Notion as human note layer, everything accessible from anywhere
- **Architecture:**
  - Obsidian (Project_P) = AI-facing memory / computer's brain
  - Notion = human notes, school, journals, thoughts
  - GitHub = code and project files
  - Claude Code = primary AI interface with 3 agents ([[ORACLE]], [[ALEX]], [[NOVA]])
  - MCP servers: Windows, Notion, Google Calendar, Gmail, Obsidian
- **Agents:**
  - **[[ORACLE]]** — research, nursing, knowledge synthesis
  - **[[ALEX]]** — filesystem, automation, local machine, system control
  - **[[NOVA]]** — Notion OS, calendar, email, digital organization
- **Session hooks:** `session-start.sh` loads brain on every Claude Code session; `end-of-session.sh` auto-commits and pushes jpate repo
- **Next steps:**
  - [x] Wire session-start hook with absolute paths
  - [x] Push hooks and settings to GitHub
  - [x] Fill in all Claude-Brain files
  - [x] Build and wire Obsidian Local REST API MCP (2026-04-07)
  - [x] Full system diagnosis — 16/16 checks passing (2026-04-10)
  - [x] Notion MCP connected and pulling context
  - [ ] Wire notes inbox → Notion sync (`sync-to-notion.py`)
  - [ ] Set up `notes/inbox/` routing to Notion DBs
  - [ ] Make supersystem accessible from iPad / other machines

## Related
- [[06-systems]]
- [[03-goals]]
- [[interests-lab]]
- [[system-state]]
- [[ORACLE]]
- [[ALEX]]
- [[NOVA]]
- [[ANI]]
