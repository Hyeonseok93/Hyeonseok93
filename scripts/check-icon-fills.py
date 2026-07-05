import base64
import re
from pathlib import Path

BADGE_DIR = Path(__file__).resolve().parent.parent / "assets" / "badges"
for path in sorted(BADGE_DIR.glob("*.svg")):
    if path.name.startswith("contact-"):
        continue
    text = path.read_text(encoding="utf-8")
    match = re.search(r"base64,([^\"]+)", text)
    if not match:
        print(f"{path.name}: no icon")
        continue
    inner = base64.b64decode(match.group(1)).decode("utf-8", "replace")
    fill = re.search(r'fill="(#[^"]+)"', inner)
    print(f"{path.name}: {fill.group(1) if fill else 'no fill'}")
