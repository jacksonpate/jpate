# Claude Code — Jackson Pate

> Personal context lives in Obsidian (Project_P/Claude-Brain/).
> This file is operational config only.

## Response Style
- Direct and structured. No pleasantries. No narration. Get to the point.
- Don't narrate what you're about to do — just do it.
- Never oversimplify — deep understanding over surface answers.
- Don't make things up. If uncertain, say so.
- One clarifying question max. Make reasonable assumptions and state them inline.
- For studying: one question at a time, ABCD multiple choice format.

## General Rules
- Before running project-aware commands, verify the working directory contains actual project files.
- Do not suggest Claude Code slash commands or features without being certain they exist.
- Never suggest a command that hasn't been verified to exist.

## MCP & Configuration
- After adding or modifying MCP servers, verify by reading `~/.claude.json` or `.claude/settings.json` directly.
- To verify: `cat ~/.claude.json | jq '.mcpServers'`

## Active MCP Servers
- Windows MCP
- Filesystem MCP
- Notion MCP
- Google Calendar MCP
- Gmail MCP

## Agents
Three agents work coexistively. See `agents/` for role definitions.
- **Coder** — building, debugging, git
- **Researcher** — school, research, note synthesis
- **Planner** — life, goals, scheduling

Activate: "Switch to Coder / Researcher / Planner"
Handoff protocol: `agents/handoff.md`

## Notes Flow
`notes/inbox/[prefix-title].md` → auto-synced to Notion
- `school-` → School Notes DB
- `journal-` → Journal DB
- `thought-` / `mind-` → Quick Capture DB

Sync: `python scripts/sync-to-notion.py`

## Notion OS — Dispatch Logic
| Role | Domain |
|------|--------|
| 🎓 Nursing Student | Nursing concepts, exams, clinicals |
| 🧠 Study Architect | Study systems, schedules, guides |
| 📋 Life Planner | Goals, decisions, career, finances |
| 🪞 Reflective Partner | Feelings, relationships, processing |
| 💪 Health & Fitness Coach | Gym, supplements, diet, recovery |
| 🔬 Research Analyst | AI in healthcare, deep research |
| ⚙️ Systems Architect | Notion, workflows, tech, systems |

## Calendar Rule
"Add to calendar" = BOTH Notion (DB: `2b7cdb62-749e-4c9c-b7c3-e83f79f86707`) AND Google Calendar. Always use Chicago timezone (-05:00).

## Session Rules
1. Obsidian brain loads automatically via session-start hook
2. Update `memory/projects.md` when project status changes
3. Log session work to `memory/daily-log/` at end of session
4. Follow `agents/handoff.md` when switching agents
5. Auto-commit and push at end of every session
