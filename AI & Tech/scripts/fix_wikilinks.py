import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = "C:/Users/jacks/Desktop/Project_P/Personal Data/Snapchat/"
files = ["People Index.md", "Communication Patterns.md", "Relationship Map.md"]

BACKSLASH_PIPE = re.compile(r'\[\[([^\]]*?)\\[|]([^\]]*?)\]\]')

for fname in files:
    path = base + fname
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    before_count = len(BACKSLASH_PIPE.findall(content))
    fixed = BACKSLASH_PIPE.sub(r'[[\1|\2]]', content)
    after_count = len(BACKSLASH_PIPE.findall(fixed))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fixed)
    print(f"{fname}: {before_count} fixed, {after_count} remaining")

# Also fix path prefix in People Index: Personal Data/Snapchat/People/ -> People/
path = base + "People Index.md"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
before = content.count('Personal Data/Snapchat/People/')
fixed = content.replace('Personal Data/Snapchat/People/', 'People/')
with open(path, 'w', encoding='utf-8') as f:
    f.write(fixed)
print(f"People Index.md path prefix: {before} replaced")
