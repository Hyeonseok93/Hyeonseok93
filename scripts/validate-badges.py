#!/usr/bin/env python3
"""Validate badge SVG labels have no %20 artifacts."""

import re
import sys
from pathlib import Path

BADGE_DIR = Path(__file__).resolve().parent.parent / "assets" / "badges"


def main() -> int:
    bad = []
    for path in sorted(BADGE_DIR.glob("*.svg")):
        if path.name.startswith("contact-"):
            continue
        text = path.read_text(encoding="utf-8")
        if "%20" in text or "%2520" in text:
            bad.append((path.name, "contains %20"))
            continue
        label = re.search(r'font-weight="bold">([^<]+)<', text)
        if label and "%" in label.group(1):
            bad.append((path.name, label.group(1)))

    if bad:
        print("BAD badges:")
        for name, reason in bad:
            print(f"  {name}: {reason}")
        return 1

    print(f"OK: {len(list(BADGE_DIR.glob('*.svg')))} badge files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
