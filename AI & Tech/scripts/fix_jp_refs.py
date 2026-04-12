import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

root = "C:/Users/jacks/Desktop/Project_P"
skip_dirs = {'.git', '.obsidian', '.vscode', '.claude'}

total = 0

for dirpath, dirnames, filenames in os.walk(root):
    # Skip hidden/system dirs
    dirnames[:] = [d for d in dirnames if d not in skip_dirs]
    for fname in filenames:
        if not fname.endswith('.md'):
            continue
        path = os.path.join(dirpath, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "Jackson's People" not in content:
            continue
        # Replace [[Jackson's People/X]] with [[People/X]]
        fixed = content.replace("[[Jackson's People/", "[[People/")
        # Also fix plain path references like (../Jackson's People/...)
        fixed = fixed.replace("../Jackson's People/", "../People/")
        fixed = fixed.replace("[Jackson's People](../Jackson's People/)", "[People](../People/)")
        if fixed != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            rel = path.replace(root + '/', '')
            print(f"Fixed: {rel}")
            total += 1

print(f"\nTotal files updated: {total}")
