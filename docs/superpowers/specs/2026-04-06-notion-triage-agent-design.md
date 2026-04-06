# Notion Triage Agent — Design Spec
**Date:** 2026-04-06  
**Status:** Approved

---

## Overview

An autonomous Python daemon that watches a Notion **Inbox** page for new Notability exports, classifies their content via Claude API, and routes everything to the correct existing Notion pages — without any manual prompting. Output pages are consistently structured to be comprehensive but never overwhelming.

---

## Flow

```
Notability → Export to Notion Inbox page
                    ↓
         Daemon polls Inbox every 60s
         (detects child pages without ✅ prefix)
                    ↓
         Claude API classifies content:
         subject, content type, chapter boundaries,
         extracted tasks, extracted dates, study guide flag
                    ↓
     ┌──────────────┬──────────────┬──────────────┬──────────┐
  Microbio       NURS 2030    NURS 2040     Task Manager  Calendar
  (child page)  (child page) (child page)  (Next Actions) (DB + GCal)
     +              +            +
  Study guide   Study guide  Study guide
  if flagged    if flagged   if flagged
                    ↓
         Inbox entry renamed to ✅ [title]
```

---

## Notion Structure

### Inbox Page (new)
- Created at root (`Jackson Pate`) — user shares all Notability exports here
- Daemon detects any child page whose title does NOT start with `✅`
- After processing: renames title to `✅ [original title]`

### Routing Destinations

| Content Detected | Destination | Notion Page ID |
|---|---|---|
| Microbiology | Child page under 🧫 Microbio | `be4e45005934493f88b6ddfa03113674` |
| NURS 2030 | Child page under 📘 NURS 2030 | `ae3d9ad3d83141c6a9e56e36fe000d42` |
| NURS 2040 | Child page under 📗 NURS 2040 | `c9511e785e0841eeb9ef8f34c47515d9` |
| Tasks / to-dos | Appended to Task Manager Next Actions checklist | `a861e1550b514fe8a532344bb1fd0036` |
| Events / dates | Calendar DB + Google Calendar | `2b7cdb62-749e-4c9c-b7c3-e83f79f86707` |
| No clear match | Child page under 🧠 Mind Vault | `10211b8f4baf4d829e49df1b6b9ce22d` |

---

## Chapter Splitting

- **One chapter in the dump** → one output page
- **Multiple chapters detected** → one page per chapter, split by Claude API using heading/section detection
- Chapter pages are named: `Chapter N — [Title]`
- Class hub pages (Microbio, NURS 2030, etc.) accumulate only linked child pages — never direct content

---

## Output Page Structure

Every generated page follows this template:

```
📌 Callout — TL;DR: 3–5 bullet key takeaways   ← always visible

▶ Toggle: Full Notes        ← verbatim/cleaned original content
▶ Toggle: Key Concepts      ← definitions, mechanisms, vocab
▶ Toggle: Study Guide       ← questions, mnemonics, tables (if flagged)
▶ Toggle: Tasks / Dates     ← anything actioned elsewhere, for reference
```

Rules:
- All detail lives inside toggles — nothing is a wall of text
- TL;DR callout is always visible without expanding anything
- Study Guide toggle only included if Claude flags the content as study material

---

## Claude API Classification

Each Inbox entry is sent to Claude API (`claude-sonnet-4-6`) with a structured prompt.

**Returns JSON:**
```json
{
  "destination": "microbiology | nurs_2030 | nurs_2040 | tasks | calendar | mind_vault",
  "chapters": [
    { "title": "Chapter 6 — Microbial Growth", "content": "..." }
  ],
  "generate_study_guide": true,
  "extracted_tasks": ["Study Lab 6 before Thursday"],
  "extracted_events": [
    { "title": "Microbio Exam 3", "date": "2026-04-15" }
  ]
}
```

---

## Daemon Architecture

### File Structure
```
JPATE/
  agent/
    agent.py            # main loop — polls, orchestrates
    classifier.py       # Claude API call + JSON parsing
    router.py           # routes classified content to handlers
    handlers/
      study.py          # creates chapter pages + study guides in Notion
      tasks.py          # appends to Task Manager Next Actions
      calendar.py       # writes to Notion Calendar DB + Google Calendar
      mind_vault.py     # fallback — dumps to Mind Vault
    notion.py           # thin Notion API wrapper
    config.py           # loads .env
    requirements.txt
  .env                  # secrets (never committed)
```

### Daemon Loop (`agent.py`)
1. Fetch Inbox child pages
2. Filter to unprocessed (title doesn't start with `✅`)
3. For each: read full content → classify → route → mark processed
4. Sleep 60s, repeat

### Config (`.env`)
```
NOTION_TOKEN=
NOTION_INBOX_PAGE_ID=
ANTHROPIC_API_KEY=
GOOGLE_CALENDAR_ID=
JPATE_ROOT=C:/Users/jacks/JPATE
POLL_INTERVAL=60
```

---

## State Sync Loop

Runs every 60s alongside triage. Reads OS state across your Notion and keeps everything coherent automatically.

### Task Manager — Completion Detection
- Reads all checkbox (to-do) blocks in Task Manager's Next Actions section
- Any checked box → delete that block from the list
- After removal → re-derives Current Focus (see below)

### Current Focus — Auto-Rewrite
- Reads remaining unchecked Next Actions + Active rows in priorities table
- Sends to Claude API → generates a new 3–5 item Current Focus summary
- Overwrites the 🔥 callout on the root `Jackson Pate` dashboard
- Result: the callout is always live — you never touch it manually

### Academic Hub — Deadline Expiry
- Reads the Key Deadlines table in Academic Hub
- Any deadline whose date has passed → marks the Notes cell as `✅ Passed`
- Does not delete rows — preserves history

### Mind Vault — Active Situations Sync
- Reads current open tasks + academic state
- Updates the active situations section in Mind Vault to reflect what's actually still in play
- Adds new situations when new tasks appear, removes them when tasks are completed

### Sync Order (per cycle)
1. Process Inbox (triage)
2. Detect completed checkboxes → remove from Next Actions
3. Expire passed deadlines in Academic Hub
4. Rewrite Current Focus callout on dashboard
5. Sync Mind Vault active situations

---

## Windows Task Scheduler

- Task name: `JPATE Triage Agent`
- Trigger: On login + repeat every 5 minutes as failsafe
- Action: `python C:/Users/jacks/JPATE/agent/agent.py`
- Logs: `agent/logs/agent.log` (rotating, max 5MB)

---

## Error Handling

- Classification failure → entry goes to Mind Vault with a `⚠️ Review needed` callout
- Notion API failure → logged, entry left unprocessed for next poll cycle
- Google Calendar failure → Calendar DB still written, GCal error logged
- Agent crash → Task Scheduler restarts it within 5 minutes

---

## Out of Scope

- Processing file attachments (PDFs, images) inside Notability exports — text content only
- Deleting existing Notion pages (only content within pages is modified)
- Two-way sync (Notion → local files)
- Detecting completion via the priorities table Status column — checkbox only
