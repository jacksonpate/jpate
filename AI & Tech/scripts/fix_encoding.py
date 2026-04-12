import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Mojibake map: Windows-1252 double-encoded artifacts -> correct UTF-8
MOJIBAKE = [
    ('\u00e2\u20ac\u201c', '\u2013'),  # â€" -> –
    ('\u00e2\u20ac\u0094', '\u2014'),  # â€" -> — (em dash variant)
    ('\u00e2\u20ac\u2122', '\u2019'),  # â€™ -> '
    ('\u00e2\u20ac\u0153', '\u201c'),  # â€œ -> "
    ('\u00e2\u20ac\u009d', '\u201d'),  # â€ -> "
    ('\u00e2\u20ac\u00a2', '\u2022'),  # â€¢ -> •
    ('\u00e2\u0086\u2019', '\u2192'),  # â†' -> →
    ('\u00e2\u20ac\u00a6', '\u2026'),  # â€¦ -> …
    ('\u00c3\u00a9', '\u00e9'),        # Ã© -> é
    ('\u00c3\u00a0', '\u00e0'),        # Ã  -> à
    ('\u00c3\u00a8', '\u00e8'),        # Ã¨ -> è
    ('\u00c3\u00bc', '\u00fc'),        # Ã¼ -> ü
]

BOM = b'\xef\xbb\xbf'

directories = [
    "C:/Users/jacks/Desktop/Project_P/Jackson's People",
    "C:/Users/jacks/Desktop/Project_P/Personal Data/Snapchat/Friends",
    "C:/Users/jacks/Desktop/Project_P/Personal Data/Snapchat/Profile",
    "C:/Users/jacks/Desktop/Project_P/Personal Data/Snapchat/Snaps",
    "C:/Users/jacks/Desktop/Project_P/Personal Data/Snapchat/People",
]

total_bom = 0
total_mojibake = 0

for directory in directories:
    if not os.path.exists(directory):
        print(f"SKIP (not found): {directory}")
        continue
    for fname in os.listdir(directory):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(directory, fname)

        # BOM strip
        with open(path, 'rb') as f:
            raw = f.read()
        had_bom = raw.startswith(BOM)
        if had_bom:
            raw = raw[3:]
            with open(path, 'wb') as f:
                f.write(raw)
            total_bom += 1

        # Mojibake fix
        try:
            content = raw.decode('utf-8')
        except UnicodeDecodeError:
            print(f"  DECODE ERROR: {fname}")
            continue

        original = content
        for bad, good in MOJIBAKE:
            content = content.replace(bad, good)

        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            total_mojibake += 1
            print(f"  MOJIBAKE fixed: {fname}")
        elif had_bom:
            print(f"  BOM stripped: {fname}")

print(f"\nDone. BOM stripped: {total_bom} files. Mojibake fixed: {total_mojibake} files.")
