# AI Supersystem — State Reference

Last updated: 2026-04-10

## Agent Network

| Agent | Role | Launch |
|-------|------|--------|
| ALEX | Filesystem, automation, local machine | `bash alex.sh` |
| NOVA | Notion OS, calendar, email | `bash nova.sh` |
| ORACLE | Research, nursing, knowledge synthesis | `bash oracle.sh` |
| ANI | Jackson — human director | — |

Identity files: `agents/identities/<NAME>.md`

## MCP Servers

| Server | Status | Notes |
|--------|--------|-------|
| Windows MCP | ✅ | `uvx windows-mcp` |
| Obsidian MCP | ✅ | Local REST API, HTTPS port 27124, custom server at `JPATE/tools/obsidian-mcp/index.js` |
| Notion MCP | ✅ | claude.ai native integration |
| Google Calendar MCP | ✅ | claude.ai native integration, America/Chicago |
| Gmail MCP | ✅ | claude.ai native integration, jacksonlukepate@gmail.com |

Configured in: `~/.claude.json` (`mcpServers` key)

## Session Hooks

| Hook | Script | Fires When |
|------|--------|-----------|
| SessionStart | `jpate/.claude/hooks/session-start.sh` | Every Claude Code session |
| Stop / EXIT | `jpate/.claude/hooks/end-of-session.sh` | Session ends |

**SessionStart loads:** `00-identity.md` in full, index paths for 01–06, Notion (cached 24h)  
**Stop hook:** Auto-commits + pushes `jpate` repo if changes exist

## Editor & Terminal

- **Primary editor:** Antigravity v1.107.0 (Google's VS Code fork, OpenVSX marketplace)
- **Terminal:** Git Bash (default in Antigravity)
- **Claude CLI:** `~/.local/bin/claude` v2.1.100
- **Antigravity extensions:** claude-code, gitlens, prettier, markdownlint, markdown-all-in-one, errorlens, todo-tree, path-intellisense
- **Install extensions:** `antigravity --install-extension <id>` (NOT `code --install-extension`)

## Vault / Repo Separation

- **Project_P** (`Desktop/Project_P`) — Obsidian vault, AI brain. Intentionally NOT a git repo.
- **jpate** (`Desktop/jpate`) — Code repo. Scripts, hooks, MCP tools. Auto-syncs to `jacksonpate/jpate`.

## Key Paths

| Thing | Path |
|-------|------|
| Vault root | `C:\Users\jacks\Desktop\Project_P` |
| jpate repo | `C:\Users\jacks\Desktop\jpate` |
| Claude global settings | `C:\Users\jacks\.claude\settings.json` |
| Claude global CLAUDE.md | `C:\Users\jacks\.claude\CLAUDE.md` |
| MCP config | `C:\Users\jacks\.claude.json` |
| Obsidian MCP server | `C:\Users\jacks\JPATE\tools\obsidian-mcp\index.js` |
| Antigravity exe | `C:\Users\jacks\AppData\Local\Programs\Antigravity\Antigravity.exe` |

## Related
- [[ALEX]]
- [[NOVA]]
- [[ORACLE]]
- [[ANI]]
- [[02-projects]]
- [[06-systems]]
