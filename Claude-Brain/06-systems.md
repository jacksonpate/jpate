# Systems & Stack

## The Setup
- **Obsidian (Project_P)** = AI brain / computer-facing memory — what Claude reads
- **Notion** = Human notes (school, journals, thoughts, mind notes) — what Jackson writes in
- **GitHub (jacksonpate)** = Code and project files
- **Claude Code** = Primary AI interface, 3 agents ([[ORACLE]], [[ALEX]], [[NOVA]])
- **Python** = Scripting and automation glue

## Agents (Project_P system)
| Agent | Role | Primary Tools |
|-------|------|---------------|
| **[[ORACLE]]** | Research, nursing, knowledge synthesis, study material | Web research, Obsidian vault |
| **[[ALEX]]** | Filesystem, automation, local machine, system control | PowerShell, Windows MCP |
| **[[NOVA]]** | Notion OS, calendar, email, digital organization | Notion MCP, Google Calendar MCP, Gmail MCP |

Agent coordination: `agents/STATUS.md`, `agents/HANDOFF.md`
Human director: **[[ANI]]**

## MCP Servers
- **Windows MCP** — system interactions (volume, processes, apps)
- **Notion MCP** — read/write Jackson's Notion workspace
- **Google Calendar MCP** — view and create events (Chicago -05:00)
- **Gmail MCP** — read, draft, search email
- **Obsidian MCP** — live vault read/write via Local REST API (HTTPS port 27124); custom server at `JPATE/tools/obsidian-mcp/index.js`; requires `NODE_TLS_REJECT_UNAUTHORIZED=0` in env

## Notion OS Structure
| Section | Purpose |
|---------|---------|
| Academic Hub | Auburn classes, coursework, notes |
| Task Manager | To-dos, weekly outcomes |
| Health Protocol | Training, recovery, nutrition |
| Mind Vault | Journaling, processing, reflection |
| Interests Lab | AI, philosophy, markets |
| Backstage > AI OS | Operating system layer |

## Session Hooks
- **SessionStart:** `session-start.sh` — loads brain context (identity, projects, memory) automatically
- **Stop:** `end-of-session.sh` — auto-commits and pushes jpate repo (no longer writes session timestamps)
- Config: `~/.claude/settings.json` with absolute paths to `jpate/.claude/hooks/`
- Session-end trap: present in both `~/.bashrc` AND `~/.bash_profile` (login shells covered)

## Notes Flow
- Drop files into `notes/inbox/[prefix-title].md`
- Prefixes route to Notion DBs: `school-` → School Notes, `journal-` → Journal, `thought-`/`mind-` → Quick Capture
- Sync script: `python scripts/sync-to-notion.py`

## Calendar Rule
"Add to calendar" = BOTH Notion (DB: `2b7cdb62-749e-4c9c-b7c3-e83f79f86707`) AND Google Calendar simultaneously. Always Chicago timezone (-05:00).

## What's Working
- Session hooks live and wired — SessionStart reads Claude-Brain + Notion context (cached 24h)
- Session-end trap in both `~/.bashrc` and `~/.bash_profile`
- Three-agent architecture fully operational ([[ORACLE]], [[ALEX]], [[NOVA]])
- Obsidian brain loads automatically on session start
- Obsidian Local REST API MCP live — 7 tools available in-session
- All MCP servers responding: Notion, Google Calendar, Gmail, Windows, Obsidian
- Git remote confirmed: `jacksonpate/jpate`
- Full system check: 16/16 passing (confirmed 2026-04-10)

## What Needs Work
- Notes inbox → Notion sync not yet deployed (`sync-to-notion.py` exists but not wired)
- iPad / remote access not yet configured

## Related
- [[02-projects]]
- [[ORACLE]]
- [[ALEX]]
- [[NOVA]]
- [[ANI]]
- [[interests-lab]]
- [[system-state]]
- [[identity]]
