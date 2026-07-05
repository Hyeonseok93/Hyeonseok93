#!/usr/bin/env python3
"""Add muted brand-colored icon strip to flat badge SVGs."""

import re
from pathlib import Path

BADGE_DIR = Path(__file__).resolve().parent.parent / "assets" / "badges"
LOGO_WIDTH = 23
TEXT_BG = "#363b44"

# Muted brand tints for the left icon strip (not eye-burning).
BRAND_COLORS = {
    "java.svg": "#8a6a3a",
    "typescript.svg": "#4a6f8f",
    "python.svg": "#4a6a85",
    "javascript.svg": "#8a7d3a",
    "c.svg": "#4a6888",
    "dart.svg": "#4a6888",
    "html5.svg": "#8a5540",
    "css3.svg": "#4a6888",
    "react.svg": "#3a6a78",
    "vite.svg": "#5a58a0",
    "tailwindcss.svg": "#4a7878",
    "mui.svg": "#4a6888",
    "tanstackquery.svg": "#8a5058",
    "zustand.svg": "#5a5550",
    "zod.svg": "#4a5888",
    "reacthookform.svg": "#8a5070",
    "recharts.svg": "#4a7878",
    "axios.svg": "#5a5088",
    "reactrouter.svg": "#8a4848",
    "flutter.svg": "#4a6888",
    "springboot.svg": "#4a7050",
    "springsecurity.svg": "#4a7050",
    "jwt.svg": "#5a5558",
    "gradle.svg": "#4a6878",
    "maven.svg": "#8a4850",
    "flyway.svg": "#8a4040",
    "sqlalchemy.svg": "#8a5040",
    "fastapi.svg": "#4a7888",
    "openapi.svg": "#4a7050",
    "postgresql.svg": "#4a6078",
    "mariadb.svg": "#4a6078",
    "redis.svg": "#8a4848",
    "docker.svg": "#4a6888",
    "nginx.svg": "#4a7050",
    "terraform.svg": "#6a5888",
    "githubactions.svg": "#4a6888",
    "pandas.svg": "#5a5070",
    "plotly.svg": "#4a6078",
    "jupyter.svg": "#8a6040",
    "streamlit.svg": "#8a4848",
    "selenium.svg": "#4a7050",
    "playwright.svg": "#4a7050",
    "beautifulsoup.svg": "#4a6e8a",
    "vitest.svg": "#5a7040",
    "qt.svg": "#4a7050",
    "opencv.svg": "#5a5088",
    "pyinstaller.svg": "#4a6e8a",
    "groq.svg": "#8a5048",
    "gemini.svg": "#6a5888",
    "antigravity.svg": "#5a5558",
    "cursor.svg": "#5a5558",
    "roberta.svg": "#8a8040",
    "huggingface.svg": "#8a8040",
}


def update_badge(path: Path, brand_color: str) -> bool:
    content = path.read_text(encoding="utf-8")
    width_match = re.search(r'width="(\d+)" height="20"', content)
    if not width_match:
        return False

    total_width = int(width_match.group(1))
    text_width = total_width - LOGO_WIDTH

    old_block = re.search(
        r'<g clip-path="url\(#r\)">'
        r'<rect width="\d+" height="20" fill="[^"]+"/>'
        r'<rect x="\d+" width="\d+" height="20" fill="[^"]+"/>'
        r'<rect width="\d+" height="20" fill="url\(#s\)"/>'
        r"</g>",
        content,
    )
    if not old_block:
        return False

    new_block = (
        f'<g clip-path="url(#r)">'
        f'<rect width="{LOGO_WIDTH}" height="20" fill="{brand_color}"/>'
        f'<rect x="{LOGO_WIDTH}" width="{text_width}" height="20" fill="{TEXT_BG}"/>'
        f'<rect width="{total_width}" height="20" fill="url(#s)"/>'
        f"</g>"
    )

    updated = content[: old_block.start()] + new_block + content[old_block.end() :]
    if updated == content:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    updated = 0
    for filename, color in sorted(BRAND_COLORS.items()):
        path = BADGE_DIR / filename
        if not path.exists():
            print(f"skip missing: {filename}")
            continue
        if update_badge(path, color):
            updated += 1
            print(f"updated: {filename}")
        else:
            print(f"no change: {filename}")

    print(f"\nDone. Updated {updated} badges.")


if __name__ == "__main__":
    main()
