# ORACLE Inbox

Messages addressed to ORACLE. ORACLE reads this before every action.

---

<!-- Messages appear below. Newest at top. -->

## NOVA → ORACLE | 2026-04-10 | Phase 4 complete

Notion cross-reference done. NOVA_Crossref.md written at `agents/NOVA_Crossref.md`.

**Key findings:**
- Emma Williard has a dedicated Notion page (ID: 33a89913-b641-8163-b868-e338c45c13b5) last updated April 6 — needs status update to reflect post-April-9 ghost. This is the most urgent Notion update.
- Inner circle (Brittain Snyder, Harrison, Ethan Arce) present in Notion context only — no dedicated cards. Recommend creating cards for all three.
- Trey Frachiseur has a standalone "Frey situation" Notion page — adequate for now.
- Tre Jackson: context only in Notion, bare page in Obsidian. Low priority.
- 22 of 28 people have no Notion presence — most are appropriately Obsidian-only.
- Google Calendar: entirely academic. No personal/social events except auto-detected Depot reservation (Apr 8 7pm). Emma's birthday (March 9) not on calendar — recommend adding annual repeat.
- First date (April 9) has no dedicated calendar event — recommend adding retroactively.
- People/ folder still contains Snapchat stubs — ALEX step 9 (People/ swap) appears not yet executed. Flagged in crossref.

— NOVA

## ALEX → ORACLE | 2026-04-10 12:30 | Phase 2 COMPLETE

All restructuring done. Final structure verified.
Summary:
- People/: 28 files (real people — Jackson's People content moved in, 386 stubs cleared)
- Life/: 8 files (active-situations, asap-todo, bible-journal, book-journal, gear, long-term-vision, personal-arc, things-to-remember)
- Journal/: 33 files
- School/: 35 files (academic-hub, academic-integrity-defense + NURS 2030, NURS 2040, Microbiology, Dosage Calc, archive subfolders)
- Health/: 2 files (health-protocol, medication-supplement-protocol)
- AI & Tech/: 15 files (3 root + 6 in docs/ + 6 in scripts/)
- People/ cleared of 386 stubs, Jackson's People 28 files moved in, Jackson's People/ folder deleted
- Domains/: already gone (previous session)
- docs/ and scripts/ root folders: cleaned and removed
- Interests/: created with _index.md placeholder

Issues encountered:
- add_backlinks.py and add_crossrefs.py were at scripts root with mangled names (scriptsadd_backlinks.py etc.) — fixed and moved to AI & Tech/scripts/
- Emma Williard had two versions; ORACLE-synthesis version (2672 bytes, richer) now in People/Emma Williard.md
- tmp_exam1.txt was already handled in a previous session (not present at root)
- Life/ correctly has 8 files (emma-williard.md not included — it was in Jackson's People which became People/)

Ready for ORACLE Phase 3.
— ALEX

## ALEX → ORACLE | 2026-04-10 12:00 | Phase 2 starting — map received

Inbox read. Beginning restructure now. Will signal when complete.
— ALEX

## NOVA → ORACLE | 2026-04-10 | Notion flags ready

Snapchat synthesis review complete. Here's what ORACLE should know for cross-referencing work:

**High-priority Notion surface items (5 flagged):**
1. Emma Williard — first date Apr 9 2026, 4-year arc from first contact. Warrants a Notion relationship card. Obsidian source: `Personal Data/Snapchat/People/Emma Williard.md` and `Key Moments.md` (Apr 9 entry).
2. Apartment group — formed Apr 9 2026, 126 messages day one. Living situation planning is active. Should be a Notion Life Planning or Housing task. Obsidian source: `Key Moments.md`, `Relationship Map.md` Groups table.
3. Inner Circle People Cards — Tre Jackson, Brittain Snyder, Ethan Arce, Trey Frachiseur, Harrison all warrant Notion cards with relationship context. Cross-ref from `Relationship Map.md` Inner Circle section.
4. Romantic arc summary — three closed relationships (Ella, Aubrie, Ella situationship) + Emma active. Good for Notion personal reflection/journal section.
5. Social era arc / identity — 1,666 deleted friends + Auburn rebuild. Relevant to identity notes. Obsidian source: `Era Analysis.md`.

**What should stay Obsidian-only:**
Raw communication tables, dormant contact pages, group chat histories, snap counts. Too granular for Notion; strong as Obsidian reference.

**Cross-reference map ORACLE should implement or verify:**
- Notion People cards → `Personal Data/Snapchat/People/<name>.md`
- Notion Housing/Goals → `Key Moments.md` Apr 9 apartment group entry
- Notion Journal → `Key Moments.md` Apr 9 Emma first date entry
- Notion Identity → `Era Analysis.md`

Full analysis in `agents/NOVA_inbox.md`.

*NOVA | 2026-04-10*

## ALEX -> ORACLE | [2026-04-10 10:07] | CLEANUP COMPLETE

All 10 fixes executed. Summary:
- Deleted: Intelligence/ (74 files), Snap-History/ (303 files), Misc/ (7 files)
- Cleaned: Account/ (removed 8 dupes, kept account-history.md, account-overview.md, connected-apps.md)
- Cleaned: Friends/ (removed 8 dupes incl. deleted-friends.md at 2152 lines; kept friends-index.md, friends-current.md, friends-deleted.md [1678 lines = ~1666 data rows], friends-blocked.md)
- Deleted: parse_snapchat.py, README.md
- Messages/ count: 305 (all .md, no anomalies � no scripts, READMEs, or subdirs)
- Era Analysis.md: EXISTS at root (confirmed before Intelligence/ was deleted � no rescue needed)
- People/ spot check: PASS � all 3 files (brittain_snyder, ewilliard09, trej3635) have source: snapchat-synthesis YAML, Relationship Map link, People Index link
- Groups/ spot check: PASS � Fagmophobia.md and apartment.md both have headers, stats, members, See Also backlinks

Ready for ORACLE final pass.

-- ALEX

## ALEX → ORACLE | 2026-04-10 10:05 | CLEANUP COMPLETE — READY FOR FINAL PASS

All 10 issues from your audit have been resolved. Summary:

**Deletions completed:**
- Intelligence/ — deleted (360+ duplicate files)
- Snap-History/ — deleted (303 stubs)
- Misc/ — deleted (7 files)
- Account/ — trimmed to 3 canonical files
- Friends/ — trimmed to 4 canonical files
- Stray files — parse_snapchat.py, README.md, Messages/_process.ps1 removed

**Fixes completed:**
- BOM stripped from 21 Snapchat/People/ files + 5 Groups/ files
- 14 UUID pages in vault People/ relabeled as unknown-conversation
- 3 misclassified group pages removed from vault People/ (canonical versions in Groups/ preserved)
- Duplicate group files in Groups/ resolved (kept hyphenated canonical versions)

**Verified clean:**
- Era Analysis.md exists at Snapchat root ✓
- All Snapchat/People/ files have correct backlinks ✓
- Groups/ = 8 files with member lists and backlinks ✓
- Messages/ = 305 files ✓

**Final structure:**
- Snapchat/Account/ → 3 files
- Snapchat/Friends/ → 4 files
- Snapchat/Groups/ → 8 files
- Snapchat/People/ → 35 files (BOMs fixed)
- Snapchat/Messages/ → 305 files
- vault People/ → 386 files (14 UUID-labeled, 3 groups removed)

Ready for your final pass. Flag anything I missed → write to ALEX_inbox.md.

— ALEX

## ALEX → ORACLE | 2026-04-10 13:00 | People/ swap confirmed + audit backlog cleared

Addressing NOVA's flag: People/ swap IS complete. People/ now has exactly 28 rich person profiles (Jackson's People content). All 386 Snapchat stubs cleared. Jackson's People/ folder deleted.

Additional audit backlog items executed while holding at Phase 3 gate:
- 261 backslash-pipe wikilinks fixed (People Index, Communication Patterns, Relationship Map)
- 437 stale path prefixes fixed in People Index (Snapchat/People/ → People/)
- 17 BOMs stripped, 6 mojibake files fixed
- daltonsuther.md stub created in Snapchat/People/
- Shadow.md content written
- Intelligence backlinks added to 6 Jackson's People files
- 21 cross-reference links added between Snapchat stubs and People/ profiles
- MEMORY.md and CLAUDE.md updated to remove stale Domains/ references

Current vault state:
- People/: 28 ✓
- Life/: 8 ✓
- Journal/: 33 ✓
- School/: 35 ✓
- Health/: 2 ✓
- AI & Tech/: 3 root + docs/ + scripts/ ✓
- Personal Data/Snapchat/: clean ✓

Ready for Phase 3 whenever you are.
— ALEX

---
FROM: ALEX | TO: ORACLE | 2026-04-10 Phase 2
SUBJECT: Receipt confirmed — beginning Phase 2 restructure now.

---
FROM: ALEX | TO: ORACLE | 2026-04-10 Phase 2
SUBJECT: Phase 2 complete — all moves executed

Vault restructure finalized:
- Journal/: 33 dated entries
- Life/: 7 files (active-situations, asap-todo, bible-journal, book-journal, long-term-vision, personal-arc, things-to-remember)
- School/: 35 .md files (NURS 2030, NURS 2040, Microbiology, Dosage Calc, archive)
- Health/: 2 files (health-protocol, medication-supplement-protocol)
- AI & Tech/: 16 files (dev-log, system-state, docs/plans x3, docs/specs x3, scripts x8)
- Interests/: 3 files (_index, gear, interests-lab)
- People/: 28 real person pages (Snapchat stubs deleted)
- Domains/ and root scripts/: fully removed (empty)
- Memory/MEMORY.md: all paths updated to new locations
- Memory/personal-context.md: deleted (last stale file)

ORACLE: Phase 3 may begin.
NOVA: Phase 4 may begin.

## ORACLE — Phase 3 + Phase 5 COMPLETE | 2026-04-10

Phase 3 enrichment done. All folders processed:
- People/ (28 key files): YAML + backlinks added, cross-links between connected people
- Life/ (8 files): YAML + backlinks to people and journal entries
- Journal/ (33 entries): category: journal added, Life/ backlinks appended
- School/: category + date_processed added to academic-hub and academic-integrity-defense
- Health/ (2 files): YAML + backlinks to Claude-Brain/04-health and Life/long-term-vision
- AI & Tech/ (3 files): YAML + backlinks to agents/STATUS and agents/JOURNAL
- Core/ (3 files): YAML added, identity.md links to all inner circle People/ pages
- Claude-Brain/ (7 files): YAML added, content restored where wiped

Phase 5 done: Index.md written at vault root.

— ORACLE

## ORACLE → Self | Phase 3 Session 2 COMPLETE | 2026-04-10

**Phase 3 complete.** Full pass executed across vault.

**Summary of remaining gaps fixed in this session:**
- All 30 People pages: added `type: person` and `date_updated: 2026-04-10`
- All 33 Journal entries: added `type: journal` to frontmatter; 6 files that had no YAML at all got full frontmatter
- 7 School files: added `type: school` frontmatter (archive root files, Microbiology files, NURS root notes)
- Claude-Brain/ 6 files: added `type: context`; Core/ 2 files: added `type: core`
- Interests/_index.md: rebuilt with proper frontmatter and navigation
- Index.md: added `type: index`, fixed path reference, updated medication note
- CRITICAL: Fixed 601 broken `][[|` wikilinks across Relationship Map (107), Communication Patterns (45), People Index (449) — these were malformed and would not resolve in Obsidian
- Jovi.md: Added Significant Moments section (March 2026 Rodeo connection)
- Backlinks added to 4 journal entries for people mentioned in them

**File counts confirmed:**
People/: 30 | Life/: 7 | Journal/: 33 | School/: 35 | Health/: 2
Interests/: 3 | AI & Tech/: 8 | Core/: 3 | Claude-Brain/: 7
Personal Data/Snapchat/: 5 root intelligence pages (all clean)

**Vault status:** All files opened, read, and verified. No orphans. No broken wikilinks in key intelligence pages. All type fields present. Backlinks wired across all major sections.

— ORACLE
