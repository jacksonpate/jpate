"""
organizer.py — File drop organizer for JPATE
Sorts loose files into categorized subfolders by extension.
Run: python organizer.py [--dry-run] [--dir PATH]
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Category map — extension → subfolder name
# ---------------------------------------------------------------------------
CATEGORIES: dict[str, str] = {
    # Documents
    ".pdf": "PDFs",
    ".doc": "Docs",
    ".docx": "Docs",
    ".odt": "Docs",
    ".rtf": "Docs",
    ".txt": "Docs",
    ".md": "Docs",
    # Spreadsheets
    ".xls": "Spreadsheets",
    ".xlsx": "Spreadsheets",
    ".csv": "Spreadsheets",
    ".ods": "Spreadsheets",
    # Presentations
    ".ppt": "Presentations",
    ".pptx": "Presentations",
    ".odp": "Presentations",
    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".svg": "Images",
    ".webp": "Images",
    ".heic": "Images",
    ".heif": "Images",
    ".tiff": "Images",
    ".tif": "Images",
    ".ico": "Images",
    # Video
    ".mp4": "Video",
    ".mov": "Video",
    ".avi": "Video",
    ".mkv": "Video",
    ".wmv": "Video",
    ".webm": "Video",
    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".aac": "Audio",
    ".flac": "Audio",
    ".ogg": "Audio",
    ".m4a": "Audio",
    # Archives
    ".zip": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".xz": "Archives",
    ".7z": "Archives",
    ".rar": "Archives",
    # Scripts / code
    ".py": "Scripts",
    ".js": "Scripts",
    ".ts": "Scripts",
    ".sh": "Scripts",
    ".bash": "Scripts",
    ".ps1": "Scripts",
    ".bat": "Scripts",
    ".rb": "Scripts",
    ".go": "Scripts",
    ".rs": "Scripts",
    ".java": "Scripts",
    ".c": "Scripts",
    ".cpp": "Scripts",
    ".h": "Scripts",
    # Data
    ".json": "Data",
    ".yaml": "Data",
    ".yml": "Data",
    ".xml": "Data",
    ".toml": "Data",
    ".ini": "Data",
    ".env": "Data",
    # Executables / installers
    ".exe": "Executables",
    ".msi": "Executables",
    ".dmg": "Executables",
    ".pkg": "Executables",
    ".deb": "Executables",
    ".rpm": "Executables",
}

# Files/dirs to never touch regardless of extension
SKIP_NAMES: frozenset[str] = frozenset(
    {
        "organizer.py",
        "CLAUDE.md",
        ".claude",
        ".git",
        ".gitignore",
        ".env",
        "__pycache__",
    }
)


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def resolve_destination(file: Path, base: Path) -> Path:
    """Return the destination path for a file, resolving name conflicts."""
    ext = file.suffix.lower()
    category = CATEGORIES.get(ext, "Misc")
    dest_dir = base / category
    dest = dest_dir / file.name

    # If a file with the same name already exists in the target, append a counter
    if dest.exists() and dest != file:
        stem, suffix = file.stem, file.suffix
        counter = 1
        while dest.exists():
            dest = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1

    return dest


def organize(base: Path, dry_run: bool = False) -> dict[str, int]:
    """
    Move loose files in `base` into categorized subfolders.
    Returns a summary dict {category: count}.
    """
    if not base.is_dir():
        raise NotADirectoryError(f"Target path is not a directory: {base}")

    summary: dict[str, int] = {}
    errors: list[str] = []

    for item in sorted(base.iterdir()):
        # Skip directories, hidden items, and protected names
        if item.name in SKIP_NAMES or item.name.startswith("."):
            logging.debug("Skipping: %s", item.name)
            continue
        if item.is_dir():
            logging.debug("Skipping directory: %s", item.name)
            continue
        if not item.is_file():
            logging.debug("Skipping non-file: %s", item.name)
            continue

        dest = resolve_destination(item, base)
        category = dest.parent.name

        logging.info("%s → %s/%s", item.name, category, dest.name)

        if not dry_run:
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(dest))
            except PermissionError:
                msg = f"Permission denied: {item}"
                logging.error(msg)
                errors.append(msg)
                continue
            except OSError as exc:
                msg = f"Failed to move {item.name}: {exc}"
                logging.error(msg)
                errors.append(msg)
                continue

        summary[category] = summary.get(category, 0) + 1

    if errors:
        logging.warning("%d file(s) could not be moved.", len(errors))

    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Organize dropped files into subfolders by type.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organizer.py                  # organize current directory
  python organizer.py --dry-run        # preview without moving anything
  python organizer.py --dir C:/Downloads
""",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path(__file__).parent,
        help="Directory to organize (default: folder containing this script)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview moves without actually moving files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show every file being processed",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)-8s %(message)s",
        stream=sys.stdout,
    )

    target = args.dir.resolve()
    logging.info("Target: %s%s", target, "  [DRY RUN]" if args.dry_run else "")

    try:
        summary = organize(target, dry_run=args.dry_run)
    except NotADirectoryError as exc:
        logging.error("%s", exc)
        return 1

    if not summary:
        logging.info("Nothing to organize.")
        return 0

    print("\nSummary:")
    for category, count in sorted(summary.items()):
        label = "(preview)" if args.dry_run else "moved"
        print(f"  {category:<20} {count:>3} file(s) {label}")
    print(f"  {'TOTAL':<20} {sum(summary.values()):>3} file(s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
