#!/usr/bin/env python3
"""
Snapchat Intelligence Map Builder
Joint operation: ALEX + NOVA + ORACLE
Date: 2026-04-10

Builds a complete relationship and communication intelligence network
from all extracted Snapchat data into the Obsidian vault.
"""

import re
import sys
import io
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Paths ─────────────────────────────────────────────────────────────────────
VAULT       = Path("C:/Users/jacks/Desktop/Project_P")
SNAP        = VAULT / "Personal Data/Snapchat"
MESSAGES    = SNAP  / "Messages"
SNAP_HIST   = SNAP  / "Snap-History"
FRIENDS_DIR = SNAP  / "Friends"
PEOPLE_DIR  = VAULT / "People"
INTEL_DIR   = SNAP  / "Intelligence"
JP_DIR      = VAULT / "Jackson's People"
TODAY       = "2026-04-10"
OWNER_TAG   = "You"   # sender label in message files for Jackson

# ── Known username → full name mappings (from Jackson's People) ───────────────
KNOWN_PEOPLE = {
    "ellazoeb":         ("Ella Zoe",       "Ella.md"),
    "aubrieee.kate":    ("Aubrie",          "Aubrie.md"),
    "brittain_snyder":  ("Brittain Snyder", "Brittain Snyder.md"),
    "ethan_arce14":     ("Ethan Arce",      "Ethan Arce.md"),
    "trej3635":         ("Tre Jackson",     "Tre Jackson.md"),
    "trey_frachiseur":  ("Trey Frachiseur", "Trey Frachiseur.md"),
    "harrison.cha7":    ("Harrison",        "Harrison.md"),
    "ewilliard09":      ("Emma Williard",   "Emma Williard.md"),
    "cpate2006":        ("Cameron Pate",    "Cameron Pate.md"),
    "dabombmom1000":    ("Angie Pate",      "Angie Pate.md"),
    "brockadams_02":    ("Brock Adams",     "Brock Adams.md"),
    "bailey_bugg06":    ("Bailey",          "Bailey Edwards.md"),
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def safe(s: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", s)

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def fm(category: str, extra: dict = None) -> str:
    lines = ["---",
             "source: snapchat-intelligence",
             f"date_processed: {TODAY}",
             f"category: {category}"]
    if extra:
        for k, v in extra.items():
            v_str = str(v).replace('"', '\\"')
            lines.append(f'{k}: "{v_str}"')
    lines += ["---", ""]
    return "\n".join(lines)

TIER_LABELS = {
    1: "Inner Circle",
    2: "Close Friend",
    3: "Regular Contact",
    4: "Occasional Contact",
    5: "Historical",
}

def tier_color(t):
    return ["", "🔴", "🟠", "🟡", "🔵", "⚫"][t]

# ── Data loaders ─────────────────────────────────────────────────────────────

def load_friends() -> dict:
    """Returns {username: {display_name, added, modified, source}}"""
    friends = {}
    for fname in ["friends-list.md", "friend-requests-sent.md", "deleted-friends.md"]:
        p = FRIENDS_DIR / fname
        if not p.exists():
            continue
        is_deleted = "deleted" in fname
        with open(p, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        in_table = False
        for line in lines:
            if "| Username |" in line:
                in_table = True
                continue
            if "|---" in line:
                continue
            if in_table and line.strip().startswith("|"):
                parts = [x.strip() for x in line.split("|")[1:-1]]
                if len(parts) >= 4:
                    uname, dname, added, *rest = parts
                    if uname and uname != "Username":
                        friends[uname] = {
                            "display_name": dname,
                            "added": added,
                            "deleted": is_deleted,
                            "source": rest[-1] if rest else "",
                        }
    return friends


def load_message_files() -> dict:
    """
    Returns {conversation_id: {
        display_name, msg_count, date_first, date_last,
        is_group, participants, messages, saved_texts
    }}
    """
    data = {}
    MSG_PAT = re.compile(
        r"\*\*(.+? UTC)\*\* — \*\*(.+?)\*\*:\s*\n(.*?)(?=\n\*\*[A-Z]|\Z)",
        re.DOTALL,
    )

    for f in MESSAGES.glob("*.md"):
        if f.stem.startswith("_"):
            continue
        with open(f, encoding="utf-8", errors="replace") as fh:
            content = fh.read()

        dn_m  = re.search(r"^display_name: (.+)$", content, re.M)
        cnt_m = re.search(r"^message_count: (\d+)$", content, re.M)
        dr_m  = re.search(r"^date_range: (.+)$", content, re.M)
        cid_m = re.search(r"^conversation_id: (.+)$", content, re.M)

        display_name = dn_m.group(1).strip()  if dn_m  else f.stem
        msg_count    = int(cnt_m.group(1))    if cnt_m else 0
        date_range   = dr_m.group(1).strip()  if dr_m  else ""
        conv_id      = cid_m.group(1).strip() if cid_m else f.stem
        is_group     = bool(re.search(r"Type.*Group Chat", content))

        # Parse date range
        date_first = date_last = ""
        if " → " in date_range:
            date_first, date_last = date_range.split(" → ", 1)

        # Parse individual messages
        messages    = []
        saved_texts = []
        participants = set()

        for m in MSG_PAT.finditer(content):
            ts, sender, body = m.group(1), m.group(2), m.group(3).strip()
            if sender == OWNER_TAG:
                sender = "jackson.pate"
            participants.add(sender)
            is_media = body.startswith("[") or not body or body == "---"
            messages.append((ts, sender, body, is_media))
            if not is_media:
                saved_texts.append((ts, sender, body))

        participants.discard("jackson.pate")
        participants.discard(OWNER_TAG)

        data[conv_id] = {
            "display_name": display_name,
            "msg_count":    msg_count,
            "date_first":   date_first,
            "date_last":    date_last,
            "is_group":     is_group,
            "participants": participants,
            "messages":     messages,
            "saved_texts":  saved_texts,
            "file_stem":    f.stem,
        }
    return data


def load_snap_files() -> dict:
    """Returns {contact: {snap_count, date_first, date_last, sent, received}}"""
    data = {}
    for f in SNAP_HIST.glob("*.md"):
        if f.stem.startswith("_"):
            continue
        with open(f, encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        c_m    = re.search(r'^contact: "?([^"\n]+)"?', content, re.M)
        tot_m  = re.search(r"\*\*Total snaps:\*\* (\d+)", content)
        sent_m = re.search(r"sent: (\d+)", content)
        recv_m = re.search(r"received: (\d+)", content)
        dr_m   = re.search(r"\*\*Date range:\*\* (.+?) → (.+)", content)

        contact    = c_m.group(1).strip()   if c_m    else f.stem
        snap_count = int(tot_m.group(1))    if tot_m  else 0
        sent       = int(sent_m.group(1))   if sent_m else 0
        received   = int(recv_m.group(1))   if recv_m else 0
        date_first = dr_m.group(1).strip()  if dr_m   else ""
        date_last  = dr_m.group(2).strip()  if dr_m   else ""

        data[contact] = {
            "snap_count": snap_count,
            "date_first": date_first,
            "date_last":  date_last,
            "sent":       sent,
            "received":   received,
        }
    return data


# ── Tier classifier ───────────────────────────────────────────────────────────
def classify_tier(msg_count: int, snap_count: int, is_known: bool, is_current_friend: bool) -> int:
    total = msg_count + snap_count
    if is_known or msg_count >= 200 or snap_count >= 500:
        return 1
    if msg_count >= 50 or snap_count >= 100 or (is_current_friend and total >= 20):
        return 2
    if msg_count >= 10 or snap_count >= 20 or is_current_friend:
        return 3
    if total > 0:
        return 4
    return 5


# ── Build unified person database ─────────────────────────────────────────────
def build_person_db(friends, messages, snaps):
    """
    Returns persons: {username/contact → {...all data...}}
    """
    persons = {}

    # Seed from friends list
    for uname, fdata in friends.items():
        persons[uname] = {
            "username":        uname,
            "display_name":    fdata["display_name"] or uname,
            "is_current":      not fdata["deleted"],
            "is_deleted":      fdata["deleted"],
            "friend_added":    fdata["added"],
            "friend_source":   fdata["source"],
            "msg_count":       0,
            "date_first_msg":  "",
            "date_last_msg":   "",
            "saved_texts":     [],
            "snap_count":      0,
            "snaps_sent":      0,
            "snaps_received":  0,
            "date_first_snap": "",
            "date_last_snap":  "",
            "groups":          [],
            "group_mates":     set(),
        }

    # Overlay message data
    for conv_id, mdata in messages.items():
        if mdata["is_group"]:
            continue
        uname = conv_id  # for DMs, conv_id = username
        if uname not in persons:
            persons[uname] = {
                "username":        uname,
                "display_name":    mdata["display_name"],
                "is_current":      False,
                "is_deleted":      False,
                "friend_added":    "",
                "friend_source":   "",
                "msg_count":       0,
                "date_first_msg":  "",
                "date_last_msg":   "",
                "saved_texts":     [],
                "snap_count":      0,
                "snaps_sent":      0,
                "snaps_received":  0,
                "date_first_snap": "",
                "date_last_snap":  "",
                "groups":          [],
                "group_mates":     set(),
            }
        p = persons[uname]
        p["msg_count"]      = mdata["msg_count"]
        p["date_first_msg"] = mdata["date_first"]
        p["date_last_msg"]  = mdata["date_last"]
        p["saved_texts"]    = mdata["saved_texts"]

    # Overlay snap data
    for contact, sdata in snaps.items():
        if contact not in persons:
            persons[contact] = {
                "username":        contact,
                "display_name":    contact,
                "is_current":      False,
                "is_deleted":      False,
                "friend_added":    "",
                "friend_source":   "",
                "msg_count":       0,
                "date_first_msg":  "",
                "date_last_msg":   "",
                "saved_texts":     [],
                "snap_count":      0,
                "snaps_sent":      0,
                "snaps_received":  0,
                "date_first_snap": "",
                "date_last_snap":  "",
                "groups":          [],
                "group_mates":     set(),
            }
        p = persons[contact]
        p["snap_count"]      = sdata["snap_count"]
        p["snaps_sent"]      = sdata["sent"]
        p["snaps_received"]  = sdata["received"]
        p["date_first_snap"] = sdata["date_first"]
        p["date_last_snap"]  = sdata["date_last"]

    # Add known people display names
    for uname, (display, jp_file) in KNOWN_PEOPLE.items():
        if uname in persons:
            # Only override if display_name looks like a username
            current = persons[uname]["display_name"]
            if current == uname or not current:
                persons[uname]["display_name"] = display

    # Overlay from friends list display names (overrides username-as-name)
    for uname, fdata in friends.items():
        if uname in persons and fdata["display_name"]:
            persons[uname]["display_name"] = fdata["display_name"]

    # Build group membership
    for conv_id, mdata in messages.items():
        if not mdata["is_group"]:
            continue
        group_name = mdata["display_name"]
        for participant in mdata["participants"]:
            if participant in persons:
                if group_name not in persons[participant]["groups"]:
                    persons[participant]["groups"].append(group_name)
                # cross-reference group mates
                for other in mdata["participants"]:
                    if other != participant:
                        persons[participant]["group_mates"].add(other)

    # Classify tiers
    for uname, p in persons.items():
        is_known = uname in KNOWN_PEOPLE
        is_current = p["is_current"]
        p["tier"] = classify_tier(p["msg_count"], p["snap_count"], is_known, is_current)

    return persons


# ── Generate person page ──────────────────────────────────────────────────────
def gen_person_page(p: dict, all_persons: dict) -> str:
    uname    = p["username"]
    display  = p["display_name"] or uname
    tier     = p["tier"]
    jp_info  = KNOWN_PEOPLE.get(uname)

    # Backlink targets
    back = "[[People/Index]] [[Snapchat/Intelligence/Relationship-Map]] [[Snapchat/Intelligence/Communication-Patterns]] [[Snapchat/Intelligence/Key-Moments]]"
    if jp_info:
        back += f" [[Jackson's People/{jp_info[1].replace('.md','')}]]"

    md  = fm("person", {"username": uname, "tier": tier, "display_name": display})
    md += f"# {display}\n\n"
    md += back + "\n\n"
    md += f"**Username:** `{uname}`  \n"
    md += f"**Tier:** {tier_color(tier)} {tier} — {TIER_LABELS[tier]}  \n"

    # Friend status
    if p["is_current"]:
        md += f"**Snapchat status:** ✅ Current friend"
        if p["friend_added"]:
            md += f" · added {p['friend_added']}"
        if p["friend_source"]:
            md += f" · _{p['friend_source']}_"
        md += "  \n"
    elif p["is_deleted"]:
        md += f"**Snapchat status:** 🗑️ Removed/deleted friend"
        if p["friend_added"]:
            md += f" · originally added {p['friend_added']}"
        md += "  \n"
    else:
        md += f"**Snapchat status:** Not in friends list  \n"

    if jp_info:
        md += f"**In Jackson's People:** [[Jackson's People/{jp_info[1].replace('.md','')}]]  \n"

    md += "\n## Communication Summary\n\n"
    md += "| Channel | Count | First | Last |\n"
    md += "|---|---|---|---|\n"
    if p["msg_count"]:
        md += f"| 💬 Messages | {p['msg_count']} | {p['date_first_msg']} | {p['date_last_msg']} |\n"
    if p["snap_count"]:
        sent = p["snaps_sent"]
        recv = p["snaps_received"]
        md += f"| 👻 Snaps | {p['snap_count']} (↑{sent} ↓{recv}) | {p['date_first_snap']} | {p['date_last_snap']} |\n"
    total = p["msg_count"] + p["snap_count"]
    md += f"\n**Total interactions:** {total}\n"

    # Saved text messages
    if p["saved_texts"]:
        md += "\n## Saved Messages\n\n"
        md += "| Date | From | Content |\n"
        md += "|---|---|---|\n"
        for ts, sender, body in p["saved_texts"]:
            from_tag = "**You**" if sender in ("jackson.pate", OWNER_TAG, "You") else sender
            # Truncate long messages
            body_cell = body[:200].replace("|", "\\|").replace("\n", " ").strip()
            if len(body) > 200:
                body_cell += "…"
            md += f"| {ts} | {from_tag} | {body_cell} |\n"

    # Group chats
    if p["groups"]:
        md += "\n## Shared Group Chats\n\n"
        for g in sorted(p["groups"]):
            gslug = safe(g)
            md += f"- [[Snapchat/Intelligence/Groups/{gslug}|{g}]]\n"

    # Group mates (people seen together in groups)
    mates = [m for m in sorted(p["group_mates"]) if m in all_persons]
    if mates:
        md += "\n## Also Seen With\n\n"
        for mate in mates[:20]:  # cap at 20 to avoid huge pages
            mate_display = all_persons[mate]["display_name"] if mate in all_persons else mate
            md += f"- [[People/{safe(mate)}|{mate_display}]]\n"
        if len(mates) > 20:
            md += f"- _(+{len(mates)-20} more)_\n"

    # Backlinks footer
    md += "\n---\n\n"
    md += "**Backlinks:** "
    md += "[[Snapchat/Intelligence/Relationship-Map|Relationship Map]] · "
    md += "[[People/Index|People Index]] · "
    md += "[[Snapchat/Intelligence/Communication-Patterns|Communication Patterns]] · "
    md += "[[Snapchat/Intelligence/Key-Moments|Key Moments]]"
    if jp_info:
        md += f" · [[Jackson's People/{jp_info[1].replace('.md','')}]]"
    md += "\n"

    return md


# ── Generate group page ───────────────────────────────────────────────────────
def gen_group_page(conv_id: str, mdata: dict, snaps: dict, persons: dict) -> str:
    name = mdata["display_name"]
    snap_data = snaps.get(name, {})

    md  = fm("group-chat", {"group_name": name, "msg_count": mdata["msg_count"]})
    md += f"# {name}\n\n"
    md += "[[People/Index]] [[Snapchat/Intelligence/Relationship-Map]] [[Snapchat/Intelligence/Communication-Patterns]]\n\n"
    md += f"**Type:** Group chat  \n"
    md += f"**Messages:** {mdata['msg_count']}  \n"
    md += f"**Date range:** {mdata['date_first']} → {mdata['date_last']}  \n"
    if snap_data:
        md += f"**Snaps:** {snap_data.get('snap_count', 0)} ({snap_data.get('date_first','')} → {snap_data.get('date_last','')})  \n"

    md += "\n## Participants\n\n"
    for p in sorted(mdata["participants"]):
        if p in persons:
            disp = persons[p]["display_name"]
            md += f"- [[People/{safe(p)}|{disp}]] (`{p}`)\n"
        else:
            md += f"- `{p}`\n"

    if mdata["saved_texts"]:
        md += "\n## Text Messages\n\n"
        md += "| Date | Sender | Content |\n"
        md += "|---|---|---|\n"
        for ts, sender, body in mdata["saved_texts"]:
            from_tag = "**You**" if sender in ("jackson.pate", OWNER_TAG, "You") else sender
            body_cell = body[:200].replace("|", "\\|").replace("\n", " ").strip()
            if len(body) > 200:
                body_cell += "…"
            md += f"| {ts} | {from_tag} | {body_cell} |\n"

    md += "\n---\n\n"
    md += "**Backlinks:** [[Snapchat/Intelligence/Relationship-Map|Relationship Map]] · [[People/Index|People Index]]\n"

    return md


# ── Relationship Map ──────────────────────────────────────────────────────────
def gen_relationship_map(persons: dict, groups: dict) -> str:
    by_tier = defaultdict(list)
    for uname, p in persons.items():
        if p["msg_count"] > 0 or p["snap_count"] > 0:
            by_tier[p["tier"]].append(p)

    for t in by_tier:
        by_tier[t].sort(key=lambda x: -(x["msg_count"] + x["snap_count"]))

    md  = fm("relationship-map")
    md += "# Snapchat Relationship Map\n\n"
    md += "[[Personal Data/Snapchat/README]] [[People/Index]] [[Snapchat/Intelligence/Communication-Patterns]] [[Snapchat/Intelligence/Key-Moments]]\n\n"
    md += f"Built from {sum(len(v) for v in by_tier.values())} contacts · {TODAY}\n\n"

    md += "## Tier System\n\n"
    md += "| Tier | Label | Criteria |\n"
    md += "|---|---|---|\n"
    md += "| 🔴 1 | Inner Circle | 200+ messages or 500+ snaps or in Jackson's People |\n"
    md += "| 🟠 2 | Close Friend | 50+ messages or 100+ snaps or current friend + active |\n"
    md += "| 🟡 3 | Regular Contact | 10+ messages or 20+ snaps or current friend |\n"
    md += "| 🔵 4 | Occasional Contact | Any activity below Tier 3 |\n"
    md += "| ⚫ 5 | Historical | Deleted friend, no remaining activity |\n\n"

    for tier in [1, 2, 3, 4]:
        people = by_tier.get(tier, [])
        if not people:
            continue
        md += f"\n## {tier_color(tier)} Tier {tier} — {TIER_LABELS[tier]} ({len(people)} people)\n\n"
        md += "| Person | Messages | Snaps | Total | Last Contact |\n"
        md += "|---|---|---|---|---|\n"
        for p in people:
            disp   = p["display_name"]
            uname  = p["username"]
            total  = p["msg_count"] + p["snap_count"]
            last   = p["date_last_msg"] or p["date_last_snap"] or "—"
            md += f"| [[People/{safe(uname)}|{disp}]] | {p['msg_count']} | {p['snap_count']} | {total} | {last} |\n"

    # Group chats section
    md += "\n## Group Chats (66)\n\n"
    grp_list = sorted(groups.items(), key=lambda x: -x[1]["msg_count"])
    md += "| Group | Messages | Date Range |\n"
    md += "|---|---|---|\n"
    for conv_id, gdata in grp_list:
        gname = gdata["display_name"]
        md += f"| [[Snapchat/Intelligence/Groups/{safe(gname)}|{gname}]] | {gdata['msg_count']} | {gdata['date_first']} → {gdata['date_last']} |\n"

    md += "\n---\n\n"
    md += "**Backlinks:** [[People/Index]] [[Snapchat/Intelligence/Communication-Patterns]] [[Snapchat/Intelligence/Key-Moments]] [[Personal Data/Snapchat/README]]\n"

    return md


# ── People Index ──────────────────────────────────────────────────────────────
def gen_people_index(persons: dict) -> str:
    md  = fm("people-index")
    md += "# People Index — Snapchat Network\n\n"
    md += "[[Snapchat/Intelligence/Relationship-Map]] [[Snapchat/Intelligence/Communication-Patterns]] [[Snapchat/Intelligence/Key-Moments]]\n\n"

    active = [(p["display_name"], p["username"], p["tier"], p["msg_count"] + p["snap_count"])
              for p in persons.values()
              if p["msg_count"] > 0 or p["snap_count"] > 0]
    active.sort(key=lambda x: (-x[2]*-1, x[0]))  # sort by tier asc, then name

    md += f"**Total active contacts:** {len(active)}\n\n"
    md += "| Name | Username | Tier | Total Interactions |\n"
    md += "|---|---|---|---|\n"
    for display, uname, tier, total in active:
        md += f"| [[People/{safe(uname)}|{display}]] | `{uname}` | {tier_color(tier)} {tier} | {total} |\n"

    md += "\n---\n\n"
    md += "**Backlinks:** [[Snapchat/Intelligence/Relationship-Map]] [[Snapchat/Intelligence/Communication-Patterns]]\n"

    return md


# ── Communication Patterns ───────────────────────────────────────────────────
def gen_communication_patterns(persons: dict, messages: dict, snaps: dict) -> str:
    # Stats
    dm_data   = {cid: m for cid, m in messages.items() if not m["is_group"]}
    grp_data  = {cid: m for cid, m in messages.items() if m["is_group"]}
    total_msgs = sum(p["msg_count"]  for p in persons.values())
    total_snps = sum(p["snap_count"] for p in persons.values())

    top_msg = sorted(
        [(p["msg_count"], p["display_name"], p["username"]) for p in persons.values() if p["msg_count"]],
        reverse=True
    )[:15]
    top_snp = sorted(
        [(p["snap_count"], p["display_name"], p["username"]) for p in persons.values() if p["snap_count"]],
        reverse=True
    )[:15]

    # Add method breakdown
    add_methods = defaultdict(int)
    for p in persons.values():
        if p["friend_source"]:
            add_methods[p["friend_source"]] += 1

    md  = fm("communication-patterns")
    md += "# Communication Patterns\n\n"
    md += "[[Snapchat/Intelligence/Relationship-Map]] [[People/Index]] [[Snapchat/Intelligence/Key-Moments]]\n\n"

    md += "## Overview\n\n"
    md += "| Metric | Value |\n"
    md += "|---|---|\n"
    md += f"| DM conversations | {len(dm_data)} |\n"
    md += f"| Group chats | {len(grp_data)} |\n"
    md += f"| Total messages logged | {total_msgs:,} |\n"
    md += f"| Total snaps logged | {total_snps:,} |\n"
    md += f"| Total unique contacts | {len([p for p in persons.values() if p['msg_count']>0 or p['snap_count']>0])} |\n"
    md += f"| Account age | Since June 3, 2020 (6 years) |\n\n"

    md += "## Top Contacts by Message Volume\n\n"
    md += "| Rank | Person | Messages | Date Range |\n"
    md += "|---|---|---|---|\n"
    for i, (count, display, uname) in enumerate(top_msg, 1):
        p = persons[uname]
        date_range = f"{p['date_first_msg']} → {p['date_last_msg']}"
        md += f"| {i} | [[People/{safe(uname)}|{display}]] | {count} | {date_range} |\n"

    md += "\n## Top Contacts by Snap Volume\n\n"
    md += "| Rank | Person | Snaps | ↑ Sent | ↓ Received |\n"
    md += "|---|---|---|---|---|\n"
    for i, (count, display, uname) in enumerate(top_snp, 1):
        p = persons[uname]
        md += f"| {i} | [[People/{safe(uname)}|{display}]] | {count} | {p['snaps_sent']} | {p['snaps_received']} |\n"

    md += "\n## How Friends Were Added\n\n"
    md += "| Method | Count |\n"
    md += "|---|---|\n"
    for method, count in sorted(add_methods.items(), key=lambda x: -x[1]):
        md += f"| {method} | {count} |\n"

    md += "\n## Group Chat Patterns\n\n"
    by_size = sorted(grp_data.items(), key=lambda x: -x[1]["msg_count"])
    md += "| Group | Messages | Participants | Topic Guess |\n"
    md += "|---|---|---|---|\n"
    topics = {
        "Bowling": "Bowling league", "Sane bowling people": "Bowling subset",
        "apartment": "Auburn apartment roommates/friends",
        "Rush": "Fraternity rush", "gruesome twosome": "Just Jackson + Tre",
        "Madison's sandals": "Friend group", "Fagmophobia": "Group chat",
        "Brady gyatt": "Brady-named group", "Bonfire Friends": "Bonfire hangout crew",
        "Robert's funeral": "Robert passed away",
        "Spring Break bitches 2.0": "Spring break trip group",
        "Money L's": "Friend group", "Chemistry": "School chem class",
        "study group": "Study group", "mommy?": "Small group",
    }
    for conv_id, gdata in by_size:
        gname = gdata["display_name"]
        pcount = len(gdata["participants"])
        topic = next((v for k, v in topics.items() if k.lower() in gname.lower()), "—")
        md += f"| [[Snapchat/Intelligence/Groups/{safe(gname)}|{gname}]] | {gdata['msg_count']} | {pcount} | {topic} |\n"

    md += "\n---\n\n"
    md += "**Backlinks:** [[Snapchat/Intelligence/Relationship-Map]] [[People/Index]] [[Snapchat/Intelligence/Key-Moments]]\n"
    md += "\nPeople discussed: " + " · ".join(
        f"[[People/{safe(p['username'])}|{p['display_name']}]]"
        for p in sorted(persons.values(), key=lambda x: -(x['msg_count']+x['snap_count']))[:20]
        if p['msg_count'] > 0 or p['snap_count'] > 0
    ) + "\n"

    return md


# ── Key Moments ───────────────────────────────────────────────────────────────
def gen_key_moments(persons: dict, messages: dict) -> str:
    md  = fm("key-moments")
    md += "# Key Moments\n\n"
    md += "[[Snapchat/Intelligence/Relationship-Map]] [[People/Index]] [[Snapchat/Intelligence/Communication-Patterns]]\n\n"
    md += "_Significant messages, long-running threads, and notable saved conversations._\n\n"

    # Oldest conversations
    md += "## Oldest Conversations\n\n"
    md += "| Person | First Message | Messages |\n"
    md += "|---|---|---|\n"
    oldest = sorted(
        [(p["date_first_msg"], p["display_name"], p["username"], p["msg_count"])
         for p in persons.values() if p["date_first_msg"]],
        key=lambda x: x[0]
    )[:15]
    for date, display, uname, count in oldest:
        md += f"| [[People/{safe(uname)}|{display}]] | {date} | {count} |\n"

    # Most recent activity
    md += "\n## Most Recently Active\n\n"
    md += "| Person | Last Message | Messages | Tier |\n"
    md += "|---|---|---|---|\n"
    recent = sorted(
        [(p["date_last_msg"], p["display_name"], p["username"], p["msg_count"], p["tier"])
         for p in persons.values() if p["date_last_msg"]],
        key=lambda x: x[0], reverse=True
    )[:20]
    for date, display, uname, count, tier in recent:
        md += f"| [[People/{safe(uname)}|{display}]] | {date} | {count} | {tier_color(tier)} {tier} |\n"

    # Notable saved texts — longest/most meaningful content
    md += "\n## Notable Saved Messages\n\n"
    md += "_Saved text messages across all conversations (non-media)._\n\n"
    all_saved = []
    for p in persons.values():
        for ts, sender, body in p.get("saved_texts", []):
            if len(body) > 20 and not body.startswith("["):
                all_saved.append((ts, p["display_name"], p["username"], sender, body))

    all_saved.sort(key=lambda x: len(x[4]), reverse=True)
    md += "| Date | Person | Sender | Message |\n"
    md += "|---|---|---|---|\n"
    for ts, display, uname, sender, body in all_saved[:50]:
        from_tag = "You" if sender in ("jackson.pate", OWNER_TAG, "You") else sender
        body_cell = body[:150].replace("|", "\\|").replace("\n", " ").strip()
        if len(body) > 150:
            body_cell += "…"
        md += f"| {ts} | [[People/{safe(uname)}|{display}]] | {from_tag} | {body_cell} |\n"

    # Group chats with real text
    md += "\n## Group Chat Highlights\n\n"
    grp_texts = []
    for conv_id, mdata in messages.items():
        if mdata["is_group"] and mdata["saved_texts"]:
            for ts, sender, body in mdata["saved_texts"]:
                if len(body) > 10:
                    grp_texts.append((ts, mdata["display_name"], conv_id, sender, body))
    grp_texts.sort(key=lambda x: len(x[4]), reverse=True)
    md += "| Date | Group | Sender | Message |\n"
    md += "|---|---|---|---|\n"
    for ts, gname, conv_id, sender, body in grp_texts[:30]:
        from_tag = "You" if sender in ("jackson.pate", OWNER_TAG, "You") else sender
        body_cell = body[:120].replace("|", "\\|").replace("\n", " ").strip()
        if len(body) > 120:
            body_cell += "…"
        md += f"| {ts} | [[Snapchat/Intelligence/Groups/{safe(gname)}|{gname}]] | {from_tag} | {body_cell} |\n"

    # People involved in key moments backlinks
    key_people = list(set(uname for _, _, uname, _, _ in all_saved[:50]))[:30]
    md += "\n---\n\n"
    md += "**People in key moments:** "
    md += " · ".join(f"[[People/{safe(u)}|{persons[u]['display_name']}]]" for u in key_people if u in persons)
    md += "\n\n"
    md += "**Backlinks:** [[Snapchat/Intelligence/Relationship-Map]] [[People/Index]] [[Snapchat/Intelligence/Communication-Patterns]]\n"

    return md


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=== Snapchat Intelligence Builder | ALEX+NOVA+ORACLE | 2026-04-10 ===\n")

    print("[1/7] Loading friends list…")
    friends = load_friends()
    print(f"      {len(friends)} friends loaded")

    print("[2/7] Loading message files…")
    messages = load_message_files()
    dm_msgs  = {k: v for k, v in messages.items() if not v["is_group"]}
    grp_msgs = {k: v for k, v in messages.items() if v["is_group"]}
    print(f"      {len(dm_msgs)} DMs + {len(grp_msgs)} group chats")

    print("[3/7] Loading snap history…")
    snaps = load_snap_files()
    print(f"      {len(snaps)} snap contacts")

    print("[4/7] Building person database…")
    persons = build_person_db(friends, messages, snaps)
    active  = [p for p in persons.values() if p["msg_count"] > 0 or p["snap_count"] > 0]
    print(f"      {len(persons)} total people | {len(active)} active")

    # Tier counts
    by_tier = defaultdict(int)
    for p in active:
        by_tier[p["tier"]] += 1
    for t in sorted(by_tier):
        print(f"      Tier {t} ({TIER_LABELS[t]}): {by_tier[t]}")

    print("\n[5/7] Writing person pages…")
    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in active:
        page  = gen_person_page(p, persons)
        fname = safe(p["username"]) + ".md"
        write(PEOPLE_DIR / fname, page)
        count += 1
    print(f"      {count} person pages written → People/")

    print("[6/7] Writing group chat pages…")
    GROUPS_DIR = INTEL_DIR / "Groups"
    GROUPS_DIR.mkdir(parents=True, exist_ok=True)
    gcount = 0
    for conv_id, mdata in grp_msgs.items():
        page  = gen_group_page(conv_id, mdata, snaps, persons)
        fname = safe(mdata["display_name"]) + ".md"
        write(GROUPS_DIR / fname, page)
        gcount += 1
    print(f"      {gcount} group pages written → Snapchat/Intelligence/Groups/")

    print("[7/7] Writing intelligence analysis pages…")
    write(INTEL_DIR / "Relationship-Map.md",      gen_relationship_map(persons, grp_msgs))
    write(INTEL_DIR / "People-Index.md",           gen_people_index(persons))
    write(INTEL_DIR / "Communication-Patterns.md", gen_communication_patterns(persons, messages, snaps))
    write(INTEL_DIR / "Key-Moments.md",            gen_key_moments(persons, messages))
    print("      Relationship-Map.md")
    print("      People-Index.md")
    print("      Communication-Patterns.md")
    print("      Key-Moments.md")

    print(f"\n=== Complete ===")
    total_files = count + gcount + 4
    print(f"Total files written: {total_files}")
    print(f"People/:                    {count} pages")
    print(f"Intelligence/Groups/:       {gcount} pages")
    print(f"Intelligence/ (analysis):   4 pages")


if __name__ == "__main__":
    main()
