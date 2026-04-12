import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

root = "C:/Users/jacks/Desktop/Project_P"

# Build set of valid People/ filenames (lowercase, no .md)
people_dir = root + "/People"
valid_people = {f[:-3].lower() for f in os.listdir(people_dir) if f.endswith('.md')}

# Build set of valid Snapchat/People stubs (lowercase, no .md)
snap_people_dir = root + "/Personal Data/Snapchat/People"
valid_snap_stubs = {f[:-3].lower() for f in os.listdir(snap_people_dir) if f.endswith('.md')}

# Pattern: [[People/TARGET]] or [[People/TARGET|ALIAS]]
# If TARGET (lowercased) is NOT in valid_people:
#   If TARGET (lowercased) IS in valid_snap_stubs: fix to [[Personal Data/Snapchat/People/TARGET|ALIAS]]
#   Else: fix to [[Personal Data/Snapchat/People/TARGET|ALIAS]] (stub doesn't exist, but at least path is right)
LINK_RE = re.compile(r'\[\[People/([^\]|]+?)((?:\|[^\]]*?)?)\]\]')

def fix_link(m):
    target = m.group(1).strip()
    alias = m.group(2)  # e.g. "|Brock Adams" or ""
    # If target matches a valid People/ file by name -> keep as [[People/target|alias]]
    if target.lower() in valid_people:
        return m.group(0)  # already correct
    # Otherwise -> send to Snapchat/People/
    return f"[[Personal Data/Snapchat/People/{target}{alias}]]"

# Files to process - the synthesis files that had the path prefix fix applied
target_files = [
    root + "/Personal Data/Snapchat/People Index.md",
    root + "/Personal Data/Snapchat/Relationship Map.md",
    root + "/Personal Data/Snapchat/Communication Patterns.md",
]

# Also scan all vault files for broken People/ username links
skip_dirs = {'.git', '.obsidian', '.vscode', '.claude'}
all_md_files = []
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in skip_dirs]
    for fname in filenames:
        if fname.endswith('.md'):
            all_md_files.append(os.path.join(dirpath, fname))

total = 0
for path in all_md_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check if there are any [[People/...]] links pointing to non-existent People/ files
    links = LINK_RE.findall(content)
    needs_fix = any(target.strip().lower() not in valid_people for target, alias in links)
    if not needs_fix:
        continue
    fixed = LINK_RE.sub(fix_link, content)
    if fixed != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        rel = path.replace(root + os.sep, '').replace(root + '/', '')
        n = sum(1 for t, a in links if t.strip().lower() not in valid_people)
        print(f"Fixed {n} links in: {rel}")
        total += 1

print(f"\nTotal files updated: {total}")
