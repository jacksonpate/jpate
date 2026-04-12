import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Map: Snapchat/People stub filename -> Jackson's People file name (if exists)
CROSSREF = {
    "aubrieee.kate.md":   "Aubrie.md",
    "aydenj0915.md":      "Ayden Smith.md",
    "baileeneal1.md":     "Bailee.md",
    "brittain_snyder.md": "Brittain Snyder.md",
    "brockadams_02.md":   "Brock Adams.md",
    "cpate2006.md":       "Cameron Pate.md",
    "elladupree22859.md": "Ella Dupree.md",
    "ethan_arce14.md":    "Ethan Arce.md",
    "evan_clay77.md":     "Evan Clay.md",
    "ewilliard09.md":     "Emma Williard.md",
    "harrison.cha7.md":   "Harrison.md",
    "kaylee_ann41706.md": "Kaylee Henderson.md",
    "miller_jolliff.md":  "Miller Jolliff.md",
    "trej3635.md":        "Tre Jackson.md",
    "trey_frachiseur.md": "Trey Frachiseur.md",
}

snap_people_dir = "C:/Users/jacks/Desktop/Project_P/Personal Data/Snapchat/People/"
jp_dir          = "C:/Users/jacks/Desktop/Project_P/Jackson's People/"
people_dir      = "C:/Users/jacks/Desktop/Project_P/People/"

updated = 0

for snap_stub, jp_name in CROSSREF.items():
    snap_path = snap_people_dir + snap_stub
    jp_path   = jp_dir + jp_name

    # 1. Add link from Snapchat stub -> Jackson's People file
    if os.path.exists(snap_path):
        with open(snap_path, 'r', encoding='utf-8') as f:
            content = f.read()
        jp_link = f"[[Jackson's People/{jp_name[:-3]}]]"
        if jp_link not in content:
            content = content.rstrip('\n') + f"\n\n## Full Profile\n- {jp_link}\n"
            with open(snap_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Snap stub updated: {snap_stub} -> {jp_name}")
            updated += 1

    # 2. Check vault People/ profile (same username) and add link if missing
    username = snap_stub[:-3]  # strip .md
    vault_path = people_dir + snap_stub
    if os.path.exists(vault_path):
        with open(vault_path, 'r', encoding='utf-8') as f:
            content = f.read()
        jp_link = f"[[Jackson's People/{jp_name[:-3]}]]"
        snap_link = f"[[Personal Data/Snapchat/People/{username}]]"
        if jp_link not in content:
            content = content.rstrip('\n') + f"\n\n## Full Profile\n- {jp_link}\n- {snap_link}\n"
            with open(vault_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Vault profile updated: People/{snap_stub}")
            updated += 1

print(f"\nTotal files updated: {updated}")
