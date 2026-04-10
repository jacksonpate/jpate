# Notion → Obsidian Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fetch all meaningful content from Jackson's Notion workspace and write it into the Obsidian vault at `C:/Users/jacks/Project_P`, organized using the ring model (Core/, Domains/).

**Architecture:** Read-only migration — Notion is never modified. Each task fetches one or more Notion pages via MCP, strips navigation chrome, and writes clean markdown to the vault. No git repo exists in Project_P, so no commits.

**Tech Stack:** Notion MCP (`mcp__claude_ai_Notion__notion-fetch`, `mcp__claude_ai_Notion__notion-query-database-view`), Write/Edit file tools, markdown.

---

## Notion Chrome Stripping Rules

Every ADHD Brain page has a repeated left-column sidebar. **Strip this entirely from all migrated content:**

```
🧠 **Ultimate ADHD Brain 2.0**
---
- [🏠 Homepage](...)
- [✅ Organize](...)
- [🧠 Brain Dumps](...)
... (any navigation list like this)
⚡ Quick Access / 📚 Tutorials (details/summary blocks)
```

Also strip:
- Column layout wrappers (just flatten the content)
- Empty template instructions like "Create sub-pages below:", "Create notes below:", "Write freely below:"
- Action buttons like "Add a Today To-Do →", "Log Daily ADHD Mind Journal"
- Notion internal links → convert to plain text (keep the label, drop the URL)
  - `[Page Title](https://www.notion.so/...)` → `Page Title`

**Preserve:** All real content — headings, body text, lists, tables, callouts with actual text, dates, emojis in headings.

---

## File Map

| Output File | Source | Notion ID |
|---|---|---|
| `Core/identity.md` | Modify existing — append Mind Vault "Who I Am" | Already fetched (use content below) |
| `Core/circle.md` | New — Mind Vault "Close Circle" | Already fetched (use content below) |
| `Domains/personal/active-situations.md` | Mind Vault "Active Situations" | Already fetched (use content below) |
| `Domains/personal/personal-arc.md` | Personal arc page | `33a89913-b641-81ad-8b3f-d308da78d20d` |
| `Domains/personal/long-term-vision.md` | Long-term vision page | `33a89913-b641-8100-99b3-f179614f31e6` |
| `Domains/personal/journal/YYYY-MM-DD-N.md` | Thought Journal (split per entry) | `33989913-b641-81f5-8077-fb0151a0c83f` |
| `Domains/personal/journals/YYYY-MM-DD-<title>.md` | Journals database entries | `779124cf-6c22-4623-948a-a3da591d938b` |
| `Domains/personal/goals/<goal-name>.md` | Goals database entries | collection: `2374b09d-eda4-41e6-aab3-4325351d8835` |
| `Domains/nursing/academic-hub.md` | Academic Hub | `a63940ef-0723-49ed-a57e-59771853e745` |
| `Domains/nursing/academic-integrity-defense.md` | Academic Integrity Defense | `32f89913-b641-8111-a050-df1890f99eaa` |
| `Domains/fitness/health-protocol.md` | Health Protocol | `3e3a78c5-dfba-489e-846b-ce27db6e9cc2` |
| `Domains/fitness/physical-health-notes.md` | Physical health notes | `33a89913-b641-81ac-b69a-e9fa4d2af653` |
| `Domains/fitness/medication-supplement-protocol.md` | Daily Medication & Supplement Protocol | `32089913-b641-8179-b958-f53e8da103ad` |
| `Domains/ai-research/interests-lab.md` | Interests Lab | `598b45a2-e6e8-4c50-8aaa-47e4e54f2c84` |

---

### Task 1: Update Core/identity.md — append deep profile

**Files:**
- Modify: `C:/Users/jacks/Project_P/Core/identity.md`

The Mind Vault "Who I Am" section has already been fetched. Append it to the existing file.

- [ ] **Step 1: Read the existing file**

Read `C:/Users/jacks/Project_P/Core/identity.md` to see current content and find the end of the file.

- [ ] **Step 2: Append the deep profile section**

Append the following content to the end of `Core/identity.md`:

```markdown

## Deep Profile

- **Archetype:** Builder/Strategist — competence-based leadership, motivated by meaning and growth
- **Values:** Integrity, loyalty, competence, growth, stability
- **Love languages:** Quality time + words of affirmation
- **Perfect day:** Gym → productive work → hang with friends → go out
- **Vision at 30:** Stable healthcare career, financial independence, strong friendships, family path, confidence
- **Core purpose:** Build something meaningful and help people
- **Ideal partner:** Emotionally intelligent, calm, loyal, God-driven
- **Processing style:** Analytical-first — works through feelings by thinking and systematizing, not venting. Feels deeply but often misread as detached.
- **Biggest fear:** Not being good enough
- **Biggest lie he tells himself:** "I should already have it figured out."
- **Stress response:** Think it through, talk it out, or channel into productivity
- **Internal story nobody sees:** Sees everyone as better than him. Keeps people at a distance — scared if they see the real him they won't like what they find. Feels like a side character in everyone else's story but wants desperately to matter.
```

- [ ] **Step 3: Verify**

Read `Core/identity.md` and confirm both the original content and the new `## Deep Profile` section are present.

---

### Task 2: Create Core/circle.md

**Files:**
- Create: `C:/Users/jacks/Project_P/Core/circle.md`

Content sourced from Mind Vault "Close Circle" — already fetched.

- [ ] **Step 1: Write the file**

Create `C:/Users/jacks/Project_P/Core/circle.md` with this content:

```markdown
# Close Circle

## Current Roommates
- Trey Frachiseur
- Brock Adams
- Kirtan Patel

## Next Year Roommates
- Trey, Brittain "Snyder", Harrison

## Closest Friends
- **Ethan Arce** — Oklahoma. Most trusted person in his life. Similar in almost every way except: not religious, sees people as beneath him (Jackson sees everyone as better than him). Even Ethan doesn't know about the "not good enough" fear.
- Tre Jackson
- Harrison
- Luke
- Brittain "Snyder"
- Trey
- Brock
- Kirtan

## Family
- **Angie Pate** — Mom. FNP. Deeply appreciated.
- **Todd Pate** — Dad. Owns a construction company.
- **Cameron** — Brother. Has spina bifida. Jackson feels he has wasted potential due to laziness, enabled by their mom.
- Doesn't share the same ideologies as his family and probably never will.
- Auburn was freedom from all of it — first time he felt truly himself.

## Romantic History
- **Aubrie** — Ex of almost 2 years. Major heartbreak, false accusations. Promise ring still worn daily (origin kept private).
- **Emma Williard** — Talked for 6 months in high school before she dated Frey. Reconnected March 6, 2026 at a bar. Talked for 4 hours. Fell asleep at her place. Treaty Oak Revival rodeo — danced, drove her home sober, asked her on a date (she said yes). First date: Wednesday April 9, The Depot, Auburn. Bringing white hydrangeas. Oval cut rings noted.
- **Ella** — Was seeing as of March 2026. Needs to end things honestly after Emma reconnect.
- **Frey** — Roommate and close friend. Dated Emma for 1.5 years. Currently has a girlfriend. Doesn't know about Jackson's feelings for Emma.
```

- [ ] **Step 2: Verify**

Read `Core/circle.md` and confirm all sections are present.

---

### Task 3: Create Domains/personal/active-situations.md

**Files:**
- Create: `C:/Users/jacks/Project_P/Domains/personal/active-situations.md`

Content sourced from Mind Vault "Active Situations" — already fetched.

- [ ] **Step 1: Create the personal subdirectory if needed**

```bash
mkdir -p "C:/Users/jacks/Project_P/Domains/personal"
```

- [ ] **Step 2: Write the file**

Create `C:/Users/jacks/Project_P/Domains/personal/active-situations.md` with this content:

```markdown
# Active Situations

## Emma Williard (Spring 2026)
Reconnected March 6 at a bar, talked 4 hours, realized feelings are real.
Order of operations: end things with Ella → figure out Emma's head → tell Frey before anything official.
First date: Wednesday April 9, The Depot, Auburn.

## The Frey Situation
Frey is roommate and Emma's ex of 1.5 years. Currently has a girlfriend. Doesn't know about Jackson's feelings.
Must be told before anything becomes official.
After the rodeo, Frey texted Emma: "wait till you fall off before you date him, he's so under me."
Jackson's response: not reacting. Living well is the answer.

## Academic Integrity Hearing
Documentation error on clinic excuse note — not misconduct.
Submitted corrected note before instructor escalated.
Strong evidence assembled. See: Domains/nursing/academic-integrity-defense.md
```

- [ ] **Step 3: Verify**

Read `Domains/personal/active-situations.md` and confirm all three situations are present.

---

### Task 4: Create Domains/personal/personal-arc.md and long-term-vision.md

**Files:**
- Create: `C:/Users/jacks/Project_P/Domains/personal/personal-arc.md`
- Create: `C:/Users/jacks/Project_P/Domains/personal/long-term-vision.md`

- [ ] **Step 1: Fetch the personal arc page**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `33a89913-b641-81ad-8b3f-d308da78d20d`

- [ ] **Step 2: Write personal-arc.md**

Strip all Notion chrome per the rules at the top of this plan. Write the clean content to `C:/Users/jacks/Project_P/Domains/personal/personal-arc.md`. Add this frontmatter at the top:

```markdown
---
source: Notion
title: Personal arc — Sept 2025 to April 2026
---
```

- [ ] **Step 3: Fetch the long-term vision page**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `33a89913-b641-8100-99b3-f179614f31e6`

- [ ] **Step 4: Write long-term-vision.md**

Strip all Notion chrome. Write clean content to `C:/Users/jacks/Project_P/Domains/personal/long-term-vision.md`. Add frontmatter:

```markdown
---
source: Notion
title: Long-term vision
---
```

- [ ] **Step 5: Verify both files**

Read both files and confirm: frontmatter present, real content present, no Notion navigation links.

---

### Task 5: Split Thought Journal into individual entry files

**Files:**
- Create: `C:/Users/jacks/Project_P/Domains/personal/journal/` (directory + files)

The Thought Journal is one large Notion page with multiple dated sections. Split each `## DATE —` heading into its own file.

- [ ] **Step 1: Fetch the Thought Journal page**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `33989913-b641-81f5-8077-fb0151a0c83f`

- [ ] **Step 2: Create the journal directory**

```bash
mkdir -p "C:/Users/jacks/Project_P/Domains/personal/journal"
```

- [ ] **Step 3: Split and write individual entry files**

For each `## DATE` section in the page, create one file. Filename format: `YYYY-MM-DD-N.md` where N is 1 (use -2 if same date appears twice, e.g. 10/27 appears twice).

Use this frontmatter template for each file:

```markdown
---
date: YYYY-MM-DD
source: Notion — Thought Journal
---

# Journal — [Original heading text]

[Entry content]
```

Entries to create (dates and filenames):
- `2025-09-27-1.md` — "9/27/25 — Saturday"
- `2025-09-28-1.md` — "9/28/25 — Sunday"
- `2025-09-29-1.md` — "9/29/25 — Monday"
- `2025-10-01-1.md` — "10/1/25 — Wednesday"
- `2025-10-13-1.md` — "10/13/25 — Monday"
- `2025-10-19-1.md` — "10/19/25 — Sunday"
- `2025-10-27-1.md` — "10/27/25" (first entry)
- `2025-10-27-2.md` — "10/27/25 — Monday Morning, 11:30am"
- `2025-10-28-1.md` — "10/28/25"
- `2025-11-02-1.md` — "11/2/25"
- `2025-11-08-1.md` — "11/8/25 — Saturday"
- `2025-11-20-1.md` — "11/20/25"
- `2025-11-22-1.md` — "11/22/25 — Saturday"
- `2025-11-23-1.md` — "11/23/25 — Sunday"
- `2025-11-27-1.md` — "11/27/25 — Thanksgiving"
- `2025-12-04-1.md` — "12/4/25 — Thursday"
- `2025-12-08-1.md` — "12/8/25 — Monday"
- `2025-10-17-1.md` — "10/17/25 — Tuesday (misdated)"
- `2026-01-29-1.md` — "1/29/26"
- `2026-02-02-1.md` — "2/2/26 — Monday"
- `2026-02-08-1.md` — "2/8/26 — Eye Exam"
- `2026-02-24-1.md` — "2/24/26"
- `2026-03-01-1.md` — "3/1/26"
- `2026-03-09-1.md` — "3/9/26"
- `2026-03-15-1.md` — "3/15/26"

Also create `2026-personal-reflections.md` for the "What Jackson Has Shared Personally" section at the bottom of the Thought Journal page:

```markdown
---
date: 2026-04-06
source: Notion — Thought Journal
---

# Personal Reflections & Identity Notes

[Content of "What Jackson Has Shared Personally" section]
```

- [ ] **Step 4: Verify**

```bash
ls "C:/Users/jacks/Project_P/Domains/personal/journal/" | wc -l
```

Expected: 26 files (25 dated entries + 1 reflections file).

---

### Task 6: Export Journals database entries

**Files:**
- Create: `C:/Users/jacks/Project_P/Domains/personal/journals/` (directory + files)

- [ ] **Step 1: Create the journals directory**

```bash
mkdir -p "C:/Users/jacks/Project_P/Domains/personal/journals"
```

- [ ] **Step 2: Query the Journals database**

Use `mcp__claude_ai_Notion__notion-query-database-view` with the Journals database ID: `779124cf-6c22-4623-948a-a3da591d938b`

Retrieve all entries. Note: if the tool returns a list of page IDs, fetch each one individually with `mcp__claude_ai_Notion__notion-fetch`.

- [ ] **Step 3: Write one file per journal entry**

For each entry, create `C:/Users/jacks/Project_P/Domains/personal/journals/YYYY-MM-DD-<slug>.md` where slug is a lowercase hyphenated version of the entry title (or type if no title).

Frontmatter for each:

```markdown
---
date: YYYY-MM-DD
type: [journal type from Notion property, e.g. "Daily ADHD Mind Journal"]
source: Notion — Journals database
---

# [Entry title or date]

[Entry content]
```

- [ ] **Step 4: Verify**

```bash
ls "C:/Users/jacks/Project_P/Domains/personal/journals/"
```

Confirm at least one file exists with frontmatter and content.

---

### Task 7: Export Goals database entries

**Files:**
- Create: `C:/Users/jacks/Project_P/Domains/personal/goals/` (directory + files)

- [ ] **Step 1: Create the goals directory**

```bash
mkdir -p "C:/Users/jacks/Project_P/Domains/personal/goals"
```

- [ ] **Step 2: Fetch the Goals database**

Use `mcp__claude_ai_Notion__notion-fetch` with data source URL: `collection://2374b09d-eda4-41e6-aab3-4325351d8835`

This will return the database schema and entries. If entries are returned as page IDs, fetch each with `mcp__claude_ai_Notion__notion-fetch`.

- [ ] **Step 3: Write one file per goal**

For each goal entry, create `C:/Users/jacks/Project_P/Domains/personal/goals/<goal-slug>.md` where slug is a lowercase hyphenated version of the goal title.

Frontmatter for each:

```markdown
---
title: [Goal title]
status: [status property from Notion if available]
source: Notion — Goals database
---

# [Goal title]

[Goal content / description]
```

- [ ] **Step 4: Verify**

```bash
ls "C:/Users/jacks/Project_P/Domains/personal/goals/"
```

Confirm files exist with frontmatter and content.

---

### Task 8: Create Domains/nursing/ files

**Files:**
- Create: `C:/Users/jacks/Project_P/Domains/nursing/academic-hub.md`
- Create: `C:/Users/jacks/Project_P/Domains/nursing/academic-integrity-defense.md`

- [ ] **Step 1: Fetch Academic Hub**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `a63940ef-0723-49ed-a57e-59771853e745`

Also check for subpages — if the page contains child pages (e.g., individual course pages), fetch those too and include their content as `## Course Name` sections within `academic-hub.md`.

- [ ] **Step 2: Write academic-hub.md**

Strip all chrome. Write to `C:/Users/jacks/Project_P/Domains/nursing/academic-hub.md` with frontmatter:

```markdown
---
source: Notion — Academic Hub
---

# Academic Hub

[Content]
```

- [ ] **Step 3: Fetch Academic Integrity Defense**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `32f89913-b641-8111-a050-df1890f99eaa`

- [ ] **Step 4: Write academic-integrity-defense.md**

Strip chrome. Write to `C:/Users/jacks/Project_P/Domains/nursing/academic-integrity-defense.md` with frontmatter:

```markdown
---
source: Notion — Academic Integrity Defense
date: 2026-spring
---

# Academic Integrity Defense — Spring 2026

[Content]
```

- [ ] **Step 5: Verify both files**

Read both files. Confirm: frontmatter present, real content present, no dead Notion links.

---

### Task 9: Create Domains/fitness/ files

**Files:**
- Create: `C:/Users/jacks/Project_P/Domains/fitness/health-protocol.md`
- Create: `C:/Users/jacks/Project_P/Domains/fitness/physical-health-notes.md`
- Create: `C:/Users/jacks/Project_P/Domains/fitness/medication-supplement-protocol.md`

- [ ] **Step 1: Fetch Health Protocol**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `3e3a78c5-dfba-489e-846b-ce27db6e9cc2`

Check for subpages — fetch and include them as sections if found.

- [ ] **Step 2: Write health-protocol.md**

Strip chrome. Write to `C:/Users/jacks/Project_P/Domains/fitness/health-protocol.md`:

```markdown
---
source: Notion — Health Protocol
---

# Health Protocol

[Content]
```

- [ ] **Step 3: Fetch Physical health notes**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `33a89913-b641-81ac-b69a-e9fa4d2af653`

- [ ] **Step 4: Write physical-health-notes.md**

Strip chrome. Write to `C:/Users/jacks/Project_P/Domains/fitness/physical-health-notes.md`:

```markdown
---
source: Notion — Physical health notes
---

# Physical Health Notes

[Content]
```

- [ ] **Step 5: Fetch Medication & Supplement Protocol**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `32089913-b641-8179-b958-f53e8da103ad`

- [ ] **Step 6: Write medication-supplement-protocol.md**

Strip chrome. Write to `C:/Users/jacks/Project_P/Domains/fitness/medication-supplement-protocol.md`:

```markdown
---
source: Notion — Daily Medication & Supplement Protocol
---

# Daily Medication & Supplement Protocol

[Content]
```

- [ ] **Step 7: Verify all three files**

Read each file. Confirm: frontmatter, real content, no Notion nav links.

---

### Task 10: Create Domains/ai-research/interests-lab.md

**Files:**
- Create: `C:/Users/jacks/Project_P/Domains/ai-research/interests-lab.md`

- [ ] **Step 1: Fetch Interests Lab**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `598b45a2-e6e8-4c50-8aaa-47e4e54f2c84`

Check for subpages — if found, fetch each and include as sections.

- [ ] **Step 2: Write interests-lab.md**

Strip chrome. Write to `C:/Users/jacks/Project_P/Domains/ai-research/interests-lab.md`:

```markdown
---
source: Notion — Interests Lab
---

# Interests Lab

[Content]
```

- [ ] **Step 3: Verify**

Read the file. Confirm: frontmatter present, real content present, no Notion nav links.

---

### Task 11: Check Archive and migrate any content found

**Files:**
- Create (if content found): `C:/Users/jacks/Project_P/Domains/personal/archive/` or appropriate Domains subfolder

- [ ] **Step 1: Fetch Archive page**

Use `mcp__claude_ai_Notion__notion-fetch` with ID: `33b89913-b641-81dd-8f64-f7813a4ee3bd`

- [ ] **Step 2: Assess content**

If the page contains only empty templates or navigation, skip and mark this task done.

If it contains real subpages or content, fetch each subpage and write to the most appropriate location in Domains/ (e.g., `Domains/personal/archive/<title>.md`).

Strip chrome and add frontmatter with `source: Notion — Archive` to each file.

- [ ] **Step 3: Verify**

If files were written, read them and confirm content is clean. If nothing was migrated, confirm the Archive page was empty/template-only.

---

### Task 12: Final vault verification

- [ ] **Step 1: List all migrated files**

```bash
find "C:/Users/jacks/Project_P" -name "*.md" -not -path "*/docs/*" -not -path "*/.obsidian/*" | sort
```

Confirm the following files exist:
```
Core/circle.md
Core/identity.md
Core/roles.md
Domains/ai-research/interests-lab.md
Domains/fitness/health-protocol.md
Domains/fitness/medication-supplement-protocol.md
Domains/fitness/physical-health-notes.md
Domains/nursing/academic-hub.md
Domains/nursing/academic-integrity-defense.md
Domains/personal/active-situations.md
Domains/personal/goals/         (≥1 file)
Domains/personal/journal/       (≥25 files)
Domains/personal/journals/      (≥1 file)
Domains/personal/long-term-vision.md
Domains/personal/personal-arc.md
Memory/MEMORY.md
```

- [ ] **Step 2: Spot-check for Notion chrome**

```bash
grep -r "notion.so" "C:/Users/jacks/Project_P/Domains/" --include="*.md" -l
```

Expected: no output (no files should contain notion.so links).

- [ ] **Step 3: Spot-check for frontmatter**

```bash
grep -rL "^---" "C:/Users/jacks/Project_P/Domains/" --include="*.md"
```

Expected: no output (all Domains/ files should have frontmatter).

Note: Core/ files intentionally have no frontmatter — only Domains/ files need it.
