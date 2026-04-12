import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = "C:/Users/jacks/Desktop/Project_P/Jackson's People/"

# People who need Relationship Map + People Index added to their Related section
needs_intel_links = [
    "Angie Pate.md",
    "Bailey Edwards.md",
    "Emma Williard.md",
    "Luke.md",
    "Todd Pate.md",
    "Tre Jackson.md",
]

INTEL_LINKS = "- [[Personal Data/Snapchat/Relationship Map]]\n- [[Personal Data/Snapchat/People Index]]"

for fname in needs_intel_links:
    path = base + fname
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'Relationship Map' in content:
        print(f"SKIP (already has link): {fname}")
        continue

    # Find ## Related section and append after the last bullet in it
    # Strategy: find ## Related, then insert links before the next ## heading or EOF
    if '## Related' in content:
        # Insert before the next section header or at end of Related block
        content = re.sub(
            r'(## Related\n(?:- \[.*\]\n?)+)',
            lambda m: m.group(0).rstrip('\n') + '\n' + INTEL_LINKS + '\n',
            content
        )
    else:
        # Append a Related section at end
        content = content.rstrip('\n') + '\n\n## Related\n' + INTEL_LINKS + '\n'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {fname}")
