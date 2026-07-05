#!/usr/bin/env python3
"""Regenerate only badges whose labels contain spaces."""

import base64
import re
import urllib.parse
import urllib.request
from pathlib import Path

BADGE_DIR = Path(__file__).resolve().parent.parent / "assets" / "badges"
BG = "363b44"

# (filename, label, logo, muted logoColor)
SPACE_BADGES = [
    ("tailwindcss.svg", "TAILWIND CSS", "tailwindcss", "6a9e98"),
    ("mui.svg", "MATERIAL UI", "mui", "7a9ec4"),
    ("tanstackquery.svg", "TANSTACK QUERY", "reactquery", "c47a82"),
    ("reacthookform.svg", "REACT HOOK FORM", "reacthookform", "c48a9c"),
    ("reactrouter.svg", "REACT ROUTER", "reactrouter", "c47a7a"),
    ("springboot.svg", "SPRING BOOT", "springboot", "7aab7a"),
    ("springsecurity.svg", "SPRING SECURITY", "springsecurity", "7aab7a"),
    ("githubactions.svg", "GITHUB ACTIONS", "githubactions", "7a9ec4"),
    ("cursor.svg", "CURSOR AI", "cursor", "c8ccd4"),
    ("huggingface.svg", "HUGGING FACE", "huggingface", "c4bc7a"),
]


def badge_url(label: str, logo: str, logo_color: str) -> str:
    url_label = label.replace(" ", "_")
    encoded = urllib.parse.quote(url_label, safe="")
    return (
        f"https://img.shields.io/badge/{encoded}-{BG}"
        f"?style=for-the-badge&logo={logo}&logoColor={logo_color}"
    )


def fix_label_text(svg: str, label: str) -> str:
    display = label.upper()
    svg = svg.replace("%20", " ")
    svg = re.sub(r'(font-weight="bold">)[^<]+(<)', rf"\g<1>{display}\g<2>", svg, count=1)
    svg = re.sub(r'(aria-label=")[^"]+(")', rf'\g<1>{display}\2', svg, count=1)
    svg = re.sub(r"(<title>)[^<]+(</title>)", rf"\g<1>{display}\g<2>", svg, count=1)
    return svg


def main() -> None:
    for filename, label, logo, logo_color in SPACE_BADGES:
        url = badge_url(label, logo, logo_color)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
        svg = fix_label_text(raw, label)

        if "%20" in svg:
            raise RuntimeError(f"{filename} still contains %20 after fix")

        text = re.search(r'font-weight="bold">([^<]+)<', svg)
        if not text or text.group(1) != label:
            raise RuntimeError(f"{filename} label mismatch: {text.group(1) if text else None}")

        path = BADGE_DIR / filename
        path.write_text(svg, encoding="utf-8")
        print(f"fixed: {filename} -> {label}")


if __name__ == "__main__":
    main()
