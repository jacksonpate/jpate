import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

root = "C:/Users/jacks/Desktop/Project_P"
people_dir = root + "/People"
skip_dirs = {'.git', '.obsidian', '.vscode', '.claude'}

# Get all People/ filenames (without .md)
people_names = {}
for fname in os.listdir(people_dir):
    if fname.endswith('.md'):
        name = fname[:-3]  # strip .md
        people_names[name.lower()] = fname  # lowercase key for matching

# Scan all vault files for wikilinks / mentions
inbound = {name: [] for name in people_names}

WIKILINK = re.compile(r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]')

for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in skip_dirs]
    for fname in filenames:
        if not fname.endswith('.md'):
            continue
        path = os.path.join(dirpath, fname)
        # Skip scanning People/ files for self-links
        if dirpath == people_dir:
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        links = WIKILINK.findall(content)
        for link in links:
            # link is the target, e.g. "Brittain Snyder" or "People/Brittain Snyder"
            # Strip path prefix
            target = link.split('/')[-1].strip().lower()
            if target in inbound:
                rel_path = path.replace(root + '/', '')
                if rel_path not in inbound[target]:
                    inbound[target].append(rel_path)

print("=== ORPHANED (0 inbound links) ===")
orphaned = []
for name_lower, sources in sorted(inbound.items()):
    if not sources:
        orphaned.append(people_names[name_lower])
        print(f"  {people_names[name_lower]}")

print(f"\n=== LINKED ({len(people_names) - len(orphaned)} files with at least 1 inbound link) ===")
for name_lower, sources in sorted(inbound.items()):
    if sources:
        print(f"  {people_names[name_lower]} ← {len(sources)} file(s)")
