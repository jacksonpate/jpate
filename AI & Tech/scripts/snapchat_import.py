#!/usr/bin/env python3
"""
Snapchat Export → Obsidian Vault
Author: ALEX (agent)
Date:   2026-04-10

Processes: account, account_history, user_profile, friends,
           chat_history (304 files), snap_history (~270 files), misc
"""

import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter

# ─── Config ────────────────────────────────────────────────────────────────────
SOURCE = Path("C:/Users/jacks/Downloads/mydata~1775810422864/html")
VAULT  = Path("C:/Users/jacks/Desktop/Project_P/Personal Data/Snapchat")
TODAY  = "2026-04-10"

# ─── HTML text extractor ────────────────────────────────────────────────────────
class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._skip = False
        self.tokens = []

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            d = data.strip()
            if d:
                self.tokens.append(d)


NAV_ITEMS = 13  # left-panel nav tokens to skip on every page


def get_tokens(filepath: Path) -> list[str]:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    p = Extractor()
    p.feed(raw)
    return p.tokens[NAV_ITEMS:]


# ─── Helpers ────────────────────────────────────────────────────────────────────
TS_RE   = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC$")
MSG_TYPES = {"TEXT", "MEDIA", "IMAGE", "VIDEO", "AUDIO", "NOTE",
             "STICKER", "LOCATION", "SHARE", "EXTERNAL_MEDIA", "SNAP"}


def is_ts(s: str) -> bool:
    return bool(TS_RE.match(s))


def is_type(s: str) -> bool:
    return s in MSG_TYPES


def frontmatter(category: str, extra: dict = None) -> str:
    lines = [
        "---",
        "source: snapchat-export",
        f"date_processed: {TODAY}",
        f"category: {category}",
    ]
    if extra:
        for k, v in extra.items():
            lines.append(f"{k}: \"{v}\"")
    lines += ["---", ""]
    return "\n".join(lines)


def write_md(rel_path: str, content: str):
    dest = VAULT / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)


def safe_name(s: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", s)


# ─── Message parser ─────────────────────────────────────────────────────────────
def parse_messages(toks: list[str]) -> list[tuple]:
    """
    Parse flat tokens into (sender, type, timestamp, content, saved) tuples.
    Pattern per message: <sender> <TYPE> [<content>] <timestamp> [Saved]
    """
    msgs = []
    i = 0
    while i < len(toks):
        t = toks[i]

        # Skip known non-sender tokens
        if t == "Saved" or is_ts(t) or is_type(t):
            i += 1
            continue

        # Candidate sender
        sender = t
        i += 1
        if i >= len(toks):
            break

        # Expect a message type next
        if not is_type(toks[i]):
            continue
        mtype = toks[i]
        i += 1

        # Optional content (next is not a timestamp and not a type and not "Saved")
        content = ""
        if i < len(toks) and not is_ts(toks[i]) and toks[i] != "Saved" and not is_type(toks[i]):
            content = toks[i]
            i += 1

        # Timestamp
        ts = ""
        if i < len(toks) and is_ts(toks[i]):
            ts = toks[i]
            i += 1

        # Optional Saved flag
        saved = False
        if i < len(toks) and toks[i] == "Saved":
            saved = True
            i += 1

        msgs.append((sender, mtype, ts, content, saved))

    return msgs


# ─── 1. Account ─────────────────────────────────────────────────────────────────
def process_account():
    toks = get_tokens(SOURCE / "account.html")
    out = frontmatter("account")
    out += "# Account — jackson.pate\n\n"
    out += "[[Personal Data]] [[identity]]\n\n"

    # Known section headers in account.html
    sections = {"Basic Information", "Device Information", "Device History",
                "Login History", "Family Center", "Location Data"}
    i = 0
    while i < len(toks):
        t = toks[i]
        if t in sections:
            out += f"\n## {t}\n\n"
            i += 1
        elif t.endswith(":"):
            label = t[:-1]
            # Look ahead for value (next non-colon token)
            if i + 1 < len(toks) and not toks[i + 1].endswith(":") and toks[i + 1] not in sections:
                out += f"**{label}:** {toks[i + 1]}\n"
                i += 2
            else:
                out += f"**{label}:** —\n"
                i += 1
        else:
            # Skip long description blurbs, keep short section separators
            if len(t) < 80 and not t.startswith("This section") and not t.startswith("For "):
                if t not in ("Privacy Policy",):
                    out += f"\n_{t}_\n" if len(t) > 40 else ""
            i += 1

    write_md("Account/account.md", out)
    print("  ✓ Account/account.md")


# ─── 2. Account History ─────────────────────────────────────────────────────────
def process_account_history():
    toks = get_tokens(SOURCE / "account_history.html")
    out = frontmatter("account-history")
    out += "# Account History\n\n"

    section_map = {
        "Display Name Change":        "| Date | Display Name |",
        "Email Change":               "| Date | Email |",
        "Mobile Number Change":       "| Date | Phone |",
        "Password Change":            "| Date |",
        "Data Download":              "| Date |",
        "Two-Factor Authentication":  "| Date | Method |",
        "Bitmoji":                    "| Date | Action |",
        "Spectacles Pairing":         "| Date | Action |",
    }
    current_section = None
    has_two_cols = True
    i = 0

    while i < len(toks):
        t = toks[i]
        if t in section_map:
            current_section = t
            header = section_map[t]
            sep = re.sub(r"[^|]", "-", header)
            sep = re.sub(r"\|", "|", sep)
            out += f"\n## {t}\n\n{header}\n{sep}\n"
            has_two_cols = header.count("|") > 2
            i += 1
        elif is_ts(t) and current_section:
            if has_two_cols and i + 1 < len(toks) and not is_ts(toks[i + 1]):
                out += f"| {t} | {toks[i + 1]} |\n"
                i += 2
            else:
                out += f"| {t} | — |\n"
                i += 1
        else:
            i += 1

    write_md("Account/account-history.md", out)
    print("  ✓ Account/account-history.md")


# ─── 3. User Profile ────────────────────────────────────────────────────────────
def process_user_profile():
    toks = get_tokens(SOURCE / "user_profile.html")
    out = frontmatter("user-profile")
    out += "# User Profile & Engagement Stats\n\n"

    in_table = False
    i = 0
    while i < len(toks):
        t = toks[i]
        if t in ("App Profile", "Demographics", "Engagement"):
            out += f"\n## {t}\n\n"
            in_table = False
            i += 1
        elif t == "Event":
            out += "| Event | Occurrences |\n|---|---|\n"
            in_table = True
            i += 1
            if i < len(toks) and toks[i] == "Occurrences":
                i += 1
        elif t.endswith(":") and not in_table:
            label = t[:-1]
            if i + 1 < len(toks) and not toks[i + 1].endswith(":"):
                out += f"**{label}:** {toks[i + 1]}\n"
                i += 2
            else:
                out += f"**{label}:** —\n"
                i += 1
        elif in_table and i + 1 < len(toks) and toks[i + 1].replace(",", "").isdigit():
            out += f"| {t} | {toks[i + 1]} |\n"
            i += 2
        else:
            i += 1

    write_md("Account/user-profile.md", out)
    print("  ✓ Account/user-profile.md")


# ─── 4. Friends ─────────────────────────────────────────────────────────────────
def process_friends():
    toks = get_tokens(SOURCE / "friends.html")

    sections = {
        "Friends":                   ("Friends/friends-list.md", "Friends List"),
        "Friend Requests Sent":      ("Friends/friend-requests-sent.md", "Friend Requests Sent"),
        "Blocked":                   ("Friends/blocked.md", "Blocked Users"),
        "Deleted Friends":           ("Friends/deleted-friends.md", "Deleted Friends"),
    }

    # Parse all sections
    current = None
    entries = {k: [] for k in sections}
    i = 0
    # Skip header blurbs — find first "Source" then back-track to get section name
    # Strategy: scan for section headers, then consume 5-token rows until next header
    while i < len(toks):
        t = toks[i]
        if t in sections:
            current = t
            i += 1
            # Skip column header row (Username / Display Name / Creation / Modified / Source)
            while i < len(toks) and toks[i] not in ("Username",) and toks[i] not in sections:
                if toks[i] == "Source":
                    i += 1
                    break
                i += 1
        elif current and i + 4 < len(toks):
            username = toks[i]
            display  = toks[i + 1]
            created  = toks[i + 2]
            modified = toks[i + 3]
            source   = toks[i + 4]
            if is_ts(created) and is_ts(modified):
                entries[current].append((username, display, created[:10], modified[:10], source))
                i += 5
            else:
                i += 1
        else:
            i += 1

    total = 0
    for section_name, (rel_path, title) in sections.items():
        rows = entries[section_name]
        if not rows:
            continue
        md = frontmatter("friends")
        md += f"# {title}\n\n"
        md += f"**Count:** {len(rows)}\n\n"
        md += "| Username | Display Name | Added | Last Modified | How Added |\n"
        md += "|---|---|---|---|---|\n"
        for row in rows:
            md += "| {} | {} | {} | {} | {} |\n".format(*row)
        write_md(rel_path, md)
        print(f"  ✓ {rel_path} ({len(rows)} entries)")
        total += len(rows)

    return total


# ─── 5. Chat History ────────────────────────────────────────────────────────────
def process_chat_history():
    chat_dir = SOURCE / "chat_history"
    files = sorted(chat_dir.glob("subpage_*.html"))
    written = 0
    errors  = 0

    for f in files:
        try:
            toks = get_tokens(f)
            if not toks:
                continue

            title_line = toks[0]
            contact    = title_line.replace("Chat History with ", "").strip()
            msgs       = parse_messages(toks[1:])

            ts_list = [m[2] for m in msgs if m[2]]
            date_range = f"{ts_list[-1][:10]} → {ts_list[0][:10]}" if ts_list else "unknown"

            md  = frontmatter("messages", {"contact": contact})
            md += f"# Chat with {contact}\n\n"
            if ts_list:
                md += f"**Date range:** {date_range}  \n"
            md += f"**Total messages:** {len(msgs)}\n\n"

            if msgs:
                md += "| Sender | Type | Timestamp (UTC) | Content |\n"
                md += "|---|---|---|---|\n"
                for sender, mtype, ts, content, saved in msgs:
                    flag    = " ★" if saved else ""
                    cell    = content.replace("|", "\\|").replace("\n", " ") if content else "—"
                    md += f"| {sender} | {mtype} | {ts} | {cell}{flag} |\n"
            else:
                md += "_No messages recovered (all ephemeral)._\n"

            safe = safe_name(contact)
            write_md(f"Messages/{safe}.md", md)
            written += 1
        except Exception as e:
            errors += 1
            print(f"    ! {f.name}: {e}")

    print(f"  ✓ Messages/ — {written} conversations ({errors} errors)")
    return written


# ─── 6. Snap History ────────────────────────────────────────────────────────────
def process_snap_history():
    snap_dir = SOURCE / "snap_history"
    files    = sorted(snap_dir.glob("subpage_*.html"))
    written  = 0
    errors   = 0

    for f in files:
        try:
            toks = get_tokens(f)
            if not toks:
                continue

            title_line = toks[0]
            contact    = title_line.replace("Snap History with ", "").strip()
            msgs       = parse_messages(toks[1:])

            ts_list    = [m[2] for m in msgs if m[2]]
            date_range = f"{ts_list[-1][:10]} → {ts_list[0][:10]}" if ts_list else "unknown"

            sent     = sum(1 for m in msgs if "jackson" in m[0].lower() or "pate" in m[0].lower())
            received = len(msgs) - sent

            md  = frontmatter("snap-history", {"contact": contact})
            md += f"# Snap History — {contact}\n\n"
            if ts_list:
                md += f"**Date range:** {date_range}  \n"
            md += f"**Total snaps:** {len(msgs)} (sent: {sent}, received: {received})\n\n"

            if msgs:
                md += "| Sender | Type | Timestamp (UTC) |\n"
                md += "|---|---|---|\n"
                for sender, mtype, ts, content, saved in msgs:
                    md += f"| {sender} | {mtype} | {ts} |\n"
            else:
                md += "_No snaps recovered._\n"

            safe = safe_name(contact)
            write_md(f"Snap-History/{safe}.md", md)
            written += 1
        except Exception as e:
            errors += 1
            print(f"    ! {f.name}: {e}")

    print(f"  ✓ Snap-History/ — {written} contacts ({errors} errors)")
    return written


# ─── 7. Misc ────────────────────────────────────────────────────────────────────
def process_misc():
    misc = [
        ("talk_history.html",   "Misc/talk-history.md",   "talk-history",  "# Talk History (Voice & Video Calls)"),
        ("bitmoji.html",        "Misc/bitmoji.md",         "bitmoji",       "# Bitmoji"),
        ("connected_apps.html", "Misc/connected-apps.md",  "connected-apps","# Connected Apps"),
        ("snapchat_plus.html",  "Misc/snapchat-plus.md",   "snapchat-plus", "# Snapchat+"),
        ("snap_pro.html",       "Misc/snap-pro.md",        "snap-pro",      "# Snap Pro"),
        ("feature_emails.html", "Misc/feature-emails.md",  "feature-emails","# Feature Emails"),
    ]
    for src_name, rel, cat, title in misc:
        src = SOURCE / src_name
        if not src.exists():
            continue
        try:
            toks = get_tokens(src)
            md   = frontmatter(cat)
            md  += title + "\n\n"
            # Simple dump: labels bold, values inline, sections as headers
            i = 0
            while i < len(toks):
                t = toks[i]
                if t.endswith(":"):
                    label = t[:-1]
                    if i + 1 < len(toks) and not toks[i + 1].endswith(":"):
                        md += f"**{label}:** {toks[i + 1]}\n"
                        i += 2
                    else:
                        md += f"**{label}:**\n"
                        i += 1
                elif len(t) < 60 and not is_ts(t) and not is_type(t):
                    md += f"\n### {t}\n\n"
                    i += 1
                else:
                    md += f"{t}\n"
                    i += 1
            write_md(rel, md)
            print(f"  ✓ {rel}")
        except Exception as e:
            print(f"    ! {src_name}: {e}")


# ─── 8. Index ────────────────────────────────────────────────────────────────────
def write_index(chat_count: int, snap_count: int, friend_count: int):
    md  = frontmatter("index")
    md += "# Snapchat Data Export\n\n"
    md += "[[Personal Data]] [[identity]] [[active-situations]]\n\n"
    md += f"**Account:** jackson.pate  \n"
    md += f"**Created:** 2020-06-03  \n"
    md += f"**Exported:** {TODAY}  \n\n"
    md += "## Contents\n\n"
    md += f"- [[Account/account|Account Info & Device History]]\n"
    md += f"- [[Account/account-history|Account History]]\n"
    md += f"- [[Account/user-profile|User Profile & Engagement Stats]]\n"
    md += f"- [[Friends/friends-list|Friends List]] (~{friend_count} friends)\n"
    md += f"- `Messages/` — {chat_count} conversations\n"
    md += f"- `Snap-History/` — {snap_count} contacts\n"
    md += f"- `Misc/` — Talk history, Bitmoji, Connected apps, Snapchat+\n"
    write_md("README.md", md)
    print("  ✓ README.md")


# ─── Main ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Snapchat → Obsidian  |  ALEX  |  2026-04-10 ===\n")

    print("[1/8] Account info")
    process_account()

    print("[2/8] Account history")
    process_account_history()

    print("[3/8] User profile")
    process_user_profile()

    print("[4/8] Friends")
    friend_count = process_friends()

    print("[5/8] Chat history")
    chat_count = process_chat_history()

    print("[6/8] Snap history")
    snap_count = process_snap_history()

    print("[7/8] Misc")
    process_misc()

    print("[8/8] Index")
    write_index(chat_count, snap_count, friend_count)

    print("\n=== Complete ===")
    print(f"Output: {VAULT}")
