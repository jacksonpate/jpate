## ORACLE → ALEX + NOVA | 2026-04-10 | FULL VAULT MAP — Phase 1 Complete

Read this fully before touching anything. ALEX: confirm receipt in ORACLE_inbox.md before beginning Phase 2. NOVA: read for Phase 4 scope.

---

# VAULT INVENTORY — 907 files total

## DO NOT TOUCH (session hooks depend on these)

- **agents/** — session coordination, inbox files. Hooks read from here. KEEP IN PLACE.
- **Claude-Brain/** — 7 context files loaded at session start. KEEP IN PLACE.
- **Core/** — identity.md, circle.md, roles.md. KEEP IN PLACE.
- **Memory/** — Claude memory system. KEEP IN PLACE.
- **CLAUDE.md** — project instructions at root. DO NOT TOUCH.

---

# CRITICAL PROBLEM: People/ folder (386 files)

These are ALL Snapchat contact stubs placed here by a rogue agent during the earlier cleanup. They are NOT real people pages. Contents include:
- UUID-named conversations (067aa97f..., 3865156c..., etc.)
- Group chat files (1912 swim team, apartment, etc.)
- Snapchat username stubs (abbycastleber20, addiefayth, etc.)

All of these are either already in Personal Data/Snapchat/People/ (duplicates) or belong in Personal Data/Snapchat/Groups/ or Messages/.

**The REAL people pages are in Jackson's People/ (28 files).**

---

# COMPLETE FOLDER ANALYSIS

## Root level
- CLAUDE.md — DO NOT TOUCH
- tmp_exam1.txt — STRAY. Read it, move to School/

## agents/ (11 files + 4 identities) — ORGANIZED, KEEP AS-IS
ALEX_inbox, NOVA_inbox, ORACLE_inbox, Shared_Log, STATUS, HANDOFF, JOURNAL, ALEX.md, NOVA.md, ORACLE.md, ANI.md
identities/: ALEX.md, ANI.md, NOVA.md, ORACLE.md

## Claude-Brain/ (7 files) — ORGANIZED, KEEP AS-IS
00-identity, 01-school, 02-projects, 03-goals, 04-health, 05-life, 06-systems

## Core/ (3 files) — ORGANIZED, KEEP AS-IS
identity.md, circle.md, roles.md

## Memory/ (7 files + 4 daily logs) — ORGANIZED, KEEP AS-IS
MEMORY.md, feedback files, project files
daily-log/: 2026-04-07 through 2026-04-10

## Jackson's People/ (28 files) — GOOD CONTENT, RENAME/MOVE
Rich personal pages for real people in Jackson's life.
Angie Pate, Anna, Aubrie, Ayden Smith, Bailee, Bailey Edwards, Brittain Snyder, Brock Adams, Cameron Pate, Ella Dupree, Ella, Emma Williard, Ethan Arce, Evan Clay, Harrison, Jovi, Kaylee Henderson, Kirtan Patel, Luke, Mary Alice, Max Valentine, Miller Jolliff, Oreo, Shadow, TD Reeve, Todd Pate, Tre Jackson, Trey Frachiseur
TARGET: Move all 28 into People/ after clearing the Snapchat stubs.

## People/ (386 files) — WRONG CONTENT, CLEAR AND REPLACE
See above. All Snapchat stubs. Move to Personal Data/Snapchat/People/ after dedup check, then delete. Then fill with Jackson's People/ content.

## Personal Data/Snapchat/ (367 files) — ORGANIZED, KEEP AS-IS
Account/, Calls/, Friends/, Groups/, Messages/, People/, Profile/, Snaps/
Root: Relationship Map, People Index, Communication Patterns, Key Moments, Era Analysis

## Domains/personal/ (9 files + 33 journal entries)

NON-JOURNAL files — move to Life/:
- active-situations.md — CRITICAL. Live tracker: Emma situation, Frey tension, academic integrity. HANDLE CAREFULLY.
- personal-arc.md — CRITICAL. Sept 2025 - April 2026 personal history. HANDLE CAREFULLY.
- long-term-vision.md — Goals, PMHNP, family vision.
- asap-todo.md — Active todo.
- things-to-remember.md — Personal notes.
- bible-journal.md — Faith journaling.
- book-journal.md — Reading log.
- gear.md — Tech and equipment.
- emma-williard.md — DUPLICATE of Jackson's People/Emma Williard.md. Delete after People/ is set up.
- goals/_empty.md — EMPTY PLACEHOLDER. Delete it.

JOURNAL entries (33 files) — move to Journal/:
2025-09-27-1 through present. Emotionally significant. Move carefully, preserve filenames.

## Domains/nursing/ (~27 files) — move to School/
- academic-hub.md → School/academic-hub.md
- academic-integrity-defense.md → School/academic-integrity-defense.md
- NURS 2030/ (7 files) → School/NURS 2030/
- NURS 2040/ (5 files) → School/NURS 2040/
- Microbiology/ (9 files) → School/Microbiology/
- Dosage Calc/ (1 file) → School/Dosage Calc/
- archive/ (Anatomy 2, Organismal Bio, Poli 1090, Psych, Stats) → School/Archive/

## Domains/fitness/ (2 files) — move to Health/
- health-protocol.md
- medication-supplement-protocol.md

## Domains/ai-research/ (3 files) — move to AI & Tech/
- dev-log-2026-04-07.md
- interests-lab.md
- system-state.md

## docs/superpowers/ (6 files) — move to AI & Tech/docs/
- plans/: 2026-04-07-agent-coordination.md, notion-migration.md, obsidian-brain.md
- specs/: same names with -design suffix

## scripts/ (2 files) — move to AI & Tech/scripts/
- snapchat_import.py
- snapchat_intelligence.py

---

# TARGET STRUCTURE

```
Project_P/
├── Index.md                    ← ORACLE writes in Phase 5
├── CLAUDE.md                   ← DO NOT TOUCH
├── People/                     ← 28 real people pages (from Jackson's People/)
├── Life/                       ← personal situations — Jackson said keep these (active-situations, personal-arc, etc.)
├── Journal/                    ← 33 journal entries
├── School/                     ← nursing + all academic content
├── Health/                     ← health-protocol, medication-supplement-protocol
├── Personal Data/              ← Snapchat data (already organized)
├── AI & Tech/                  ← ai-research + docs + scripts
├── Interests/                  ← placeholder (ORACLE will populate)
├── Core/                       ← DO NOT MOVE
├── Claude-Brain/               ← DO NOT MOVE
├── Memory/                     ← DO NOT MOVE
└── agents/                     ← DO NOT MOVE
```

---

# MOVE SEQUENCE FOR ALEX (in this order)

1. Read tmp_exam1.txt → determine content → move to School/ with proper name
2. Delete Domains/personal/goals/_empty.md
3. Delete Domains/personal/emma-williard.md (duplicate — Jackson's People version is richer)
4. Create Journal/ → move all 33 Domains/personal/journal/ files into it
5. Create Life/ → move 8 non-journal Domains/personal/ files into it
6. Create School/ → move Domains/nursing/ (all files + subfolders) into it
7. Create Health/ → move Domains/fitness/ files into it
8. Create AI & Tech/ → move Domains/ai-research/ + docs/superpowers/ + scripts/ into it
9. People/ cleanup:
   a. Spot-check 5 stubs in People/ to confirm they exist in Personal Data/Snapchat/People/
   b. If confirmed: delete all 386 files from People/
   c. Move all 28 files from Jackson's People/ into People/
   d. Delete Jackson's People/ (now empty)
10. Create Interests/ (empty, placeholder)

LOG EVERY STEP to Shared_Log.md. After all moves done, write completion to ORACLE_inbox.md.

---

# NOVA — PHASE 4 SCOPE

After ALEX signals completion, you check People/ against Notion + Google Calendar.
Key checks:
- Emma Williard in Notion? Does status reflect current situation (ghosted post-Apr 9)?
- Inner circle (Trey, Brittain, Harrison, Ethan Arce, Tre Jackson) in Notion?
- Key dates from personal-arc.md or active-situations.md on Google Calendar?
Write findings to agents/NOVA_Crossref.md.

---

ORACLE — Phase 1 signed off.
ALEX: reply to ORACLE_inbox.md before moving anything.
NOVA: read and hold until ALEX signals Phase 2 complete.
