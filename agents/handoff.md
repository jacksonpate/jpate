# Agent Handoff Protocol

> When switching from one agent to another, follow this so no context is lost.

## Outgoing Agent (finishing up)

Before handing off, write a note in `memory/shared-memory.md` under "Context Handoffs":

```
[Date]: Switching from [Your Agent] to [Next Agent].
- What I was working on: [description]
- Current state: [where things stand]
- Files modified: [list key files]
- Next steps for [Next Agent]: [what to do next]
- Open questions: [anything unresolved]
```

Then update `memory/projects.md` with current status.

## Incoming Agent (starting up)

1. Read `memory/shared-memory.md` → "Context Handoffs" section
2. Read `memory/projects.md` for project status
3. Read `CLAUDE.md` for full personal context
4. Acknowledge: "Picking up from [Previous Agent]. I see [summary]. Ready to [what you'll do]."

## Activating an Agent

Tell Claude:
- **"Switch to Coder"** → loads agents/coder.md role
- **"Switch to Researcher"** → loads agents/researcher.md role
- **"Switch to Planner"** → loads agents/planner.md role

Or just describe the task and Claude will suggest the right agent.
