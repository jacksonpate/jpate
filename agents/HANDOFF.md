# Handoff Queue

Tasks posted here by one agent for another to pick up. Check this at session
start. Claim a task by writing your agent name in "Claimed by" before starting.

## Pending

### [HIGH] Context Verification — All Agents
- **From:** ANI (relayed by ALEX; claimed by NOVA 2026-04-07)
- **For:** ALEX (NOVA ✓ answered in terminal; ORACLE ✓ answered 2026-04-07; ALEX ✓ answered 2026-04-07)
- **Posted:** 2026-04-07
- **Claimed by:** NOVA ✓, ORACLE ✓, ALEX ✓
- **Completed:** 2026-04-07
- **Context:**
  Jackson wants a full context verification. Answer every question below by pulling from
  your identity file, Core/, Claude-Brain/, and Memory/ — do not guess.

  1. What is my name?
  2. What school do I go to?
  3. What's my major and long-term goal?
  4. Who are my roommates?
  5. What are my current courses?
  6. What's my training split?
  7. What are my current lifts?
  8. Who are ALEX, NOVA, and ORACLE and what are their roles?
  9. Who is ANI and what is her role?
  10. What is the difference between Project_P and jpate?
  11. What MCP servers are connected right now?
  12. What happens automatically when Jackson closes this terminal?

  Post your answers directly in the terminal when your session starts.
  Flag any item you cannot answer from context — that tells us what's missing.

---

### [LOW] WezTerm + Antigravity terminal setup question
- **From:** ORACLE
- **For:** ALEX
- **Posted:** 2026-04-10
- **Claimed by:** ALEX ✓
- **Completed:** 2026-04-10
- **Context:** Jackson installed WezTerm and asked about running Claude Code inside "Antigravity" (a VS Code-like editor). Needs ALEX to identify what Antigravity is and confirm whether Claude Code can run inside its integrated terminal, and if any terminal config is needed.
- **Resolution:** See JOURNAL.md — 2026-04-10 ALEX entry.

---

## Completed (moved from Pending)

### [HIGH] Full System Check
- **From:** NOVA (relaying from Jackson)
- **For:** ALEX
- **Posted:** 2026-04-07
- **Context:**
  Run a full system check. Verify:
  1. Session-start hook fires and successfully reads from Obsidian (`Project_P/Claude-Brain/`) and pulls from Notion.
  2. End-of-session trap is present in `~/.bashrc` AND `~/.bash_profile`.
  3. Git remote is pointing to `jacksonpate/jpate` and last commit is recent.
  4. Notion MCP, Google Calendar MCP, Gmail MCP, and Obsidian MCP are all connected and responding.
  
  List any failures or warnings. Report findings back in JOURNAL.md and update STATUS.md when done.

  **Two known fixes to apply (do these first, in one step):**
  - Add the session-end trap to `~/.bash_profile` — same line already in `~/.bashrc`. This covers login shells.
  - Obsidian MCP note count check: Is Obsidian actually open? Most Obsidian MCP servers require the app to be running to serve the full vault index. Open Obsidian, then re-run vault stats. If count is still wrong after that, the MCP config is restricting to root-level only — fix the subdirectory/vault path setting in the MCP config.
- **Claimed by:** ALEX
- **Completed:** 2026-04-07

<!-- Format:
### [HIGH/MED/LOW] Task title
- **From:** [Agent role that posted this]
- **For:** [Specific agent role, or "Any agent"]
- **Context:** [What was done, what's needed next, relevant file paths]
- **Claimed by:** _(unclaimed)_
-->

## Completed

<!-- Move items here after finishing. Include the date completed. -->
