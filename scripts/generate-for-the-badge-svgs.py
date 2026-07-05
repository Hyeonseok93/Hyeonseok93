#!/usr/bin/env python3
"""Download for-the-badge style shields as local SVG files."""

import base64
import re
import urllib.parse
import urllib.request
from pathlib import Path

BADGE_DIR = Path(__file__).resolve().parent.parent / "assets" / "badges"
BG = "363b44"

GROQ_PATH = (
    "m128 49 1.895 1.52C136.336 56.288 140.602 64.49 142 73c.097 1.823.148 3.648.161 5.474"
    "l.03 3.247.012 3.482.017 3.613c.01 2.522.016 5.044.02 7.565.01 3.84.041 7.68.072 11.521"
    ".007 2.455.012 4.91.016 7.364l.038 3.457c-.033 11.717-3.373 21.83-11.475 30.547-4.552 4.23"
    "-9.148 7.372-14.891 9.73l-2.387 1.055c-9.275 3.355-20.3 2.397-29.379-1.13-5.016-2.38-9.156"
    "-5.17-13.234-8.925 3.678-4.526 7.41-8.394 12-12l3.063 2.375c5.572 3.958 11.135 5.211 17.937"
    " 4.625 6.96-1.384 12.455-4.502 17-10 4.174-6.784 4.59-12.222 4.531-20.094l.012-3.473c.003"
    "-2.414-.005-4.827-.022-7.241-.02-3.68 0-7.36.026-11.04-.003-2.353-.008-4.705-.016-7.058l"
    ".025-3.312c-.098-7.996-1.732-13.21-6.681-19.47-6.786-5.458-13.105-8.211-21.914-7.792-7.327"
    " 1.188-13.278 4.7-17.777 10.601C75.472 72.012 73.86 78.07 75 85c2.191 7.547 5.019 13.948 12"
    " 18 5.848 3.061 10.892 3.523 17.438 3.688l2.794.103c2.256.082 4.512.147 6.768.209v16c-16.682"
    ".673-29.615.654-42.852-10.848-8.28-8.296-13.338-19.55-13.71-31.277.394-9.87 3.93-17.894 9.562"
    "-25.875l1.688-2.563C84.698 35.563 110.05 34.436 128 49Z"
)

# (filename, label with real spaces, logo or None, muted logoColor)
BADGES = [
    ("java.svg", "JAVA", "openjdk", "c4a574"),
    ("typescript.svg", "TYPESCRIPT", "typescript", "7aabcc"),
    ("python.svg", "PYTHON", "python", "8aacbf"),
    ("javascript.svg", "JAVASCRIPT", "javascript", "c4bc7a"),
    ("c.svg", "C", "c", "7a9ec4"),
    ("dart.svg", "DART", "dart", "7a9ec4"),
    ("html5.svg", "HTML5", "html5", "c4907a"),
    ("css3.svg", "CSS3", "css3", "7a9ec4"),
    ("react.svg", "REACT", "react", "6a9aaa"),
    ("vite.svg", "VITE", "vite", "8a8ccc"),
    ("tailwindcss.svg", "TAILWIND CSS", "tailwindcss", "6a9e98"),
    ("mui.svg", "MATERIAL UI", "mui", "7a9ec4"),
    ("tanstackquery.svg", "TANSTACK QUERY", "reactquery", "c47a82"),
    ("zustand.svg", "ZUSTAND", "react", "c8ccd4"),
    ("zod.svg", "ZOD", "zod", "7a8cbb"),
    ("reacthookform.svg", "REACT HOOK FORM", "reacthookform", "c48a9c"),
    ("recharts.svg", "RECHARTS", "react", "6a9eaa"),
    ("axios.svg", "AXIOS", "axios", "8a82c4"),
    ("reactrouter.svg", "REACT ROUTER", "reactrouter", "c47a7a"),
    ("flutter.svg", "FLUTTER", "flutter", "7a9ec4"),
    ("springboot.svg", "SPRING BOOT", "springboot", "7aab7a"),
    ("springsecurity.svg", "SPRING SECURITY", "springsecurity", "7aab7a"),
    ("jwt.svg", "JWT", "jsonwebtokens", "c8ccd4"),
    ("gradle.svg", "GRADLE", "gradle", "6a9aaa"),
    ("maven.svg", "MAVEN", "apachemaven", "c47a82"),
    ("flyway.svg", "FLYWAY", "flyway", "c47a7a"),
    ("sqlalchemy.svg", "SQLALCHEMY", "sqlalchemy", "c48a7a"),
    ("fastapi.svg", "FASTAPI", "fastapi", "6a9aaa"),
    ("openapi.svg", "OPENAPI", "openapiinitiative", "7aab7a"),
    ("postgresql.svg", "POSTGRESQL", "postgresql", "6a8aaa"),
    ("mariadb.svg", "MARIADB", "mariadb", "6a9aaa"),
    ("redis.svg", "REDIS", "redis", "c47a7a"),
    ("docker.svg", "DOCKER", "docker", "6a9ec4"),
    ("nginx.svg", "NGINX", "nginx", "7aab7a"),
    ("terraform.svg", "TERRAFORM", "terraform", "9a8aab"),
    ("githubactions.svg", "GITHUB ACTIONS", "githubactions", "7a9ec4"),
    ("pandas.svg", "PANDAS", "pandas", "8a82aa"),
    ("plotly.svg", "PLOTLY", "plotly", "7a8aaa"),
    ("jupyter.svg", "JUPYTER", "jupyter", "c4907a"),
    ("streamlit.svg", "STREAMLIT", "streamlit", "c47a7a"),
    ("selenium.svg", "SELENIUM", "selenium", "7aab7a"),
    ("playwright.svg", "PLAYWRIGHT", "playwright", "7aab7a"),
    ("beautifulsoup.svg", "BEAUTIFULSOUP", "python", "8aacbf"),
    ("vitest.svg", "VITEST", "vitest", "8aab6a"),
    ("qt.svg", "QT", "qt", "7aab7a"),
    ("opencv.svg", "OPENCV", "opencv", "8a82c4"),
    ("pyinstaller.svg", "PYINSTALLER", "python", "8aacbf"),
    ("gemini.svg", "GEMINI", "googlegemini", "9a8aab"),
    ("antigravity.svg", "ANTIGRAVITY", "google", "7a9ec4"),
    ("cursor.svg", "CURSOR AI", "cursor", "c8ccd4"),
    ("roberta.svg", "ROBERTA", "huggingface", "c4bc7a"),
    ("huggingface.svg", "HUGGING FACE", "huggingface", "c4bc7a"),
]


def badge_url(label: str, logo: str | None, logo_color: str) -> str:
    # shields treats underscores as spaces in the rendered label.
    url_label = label.replace(" ", "_")
    encoded_label = urllib.parse.quote(url_label, safe="")
    url = f"https://img.shields.io/badge/{encoded_label}-{BG}?style=for-the-badge"
    if logo:
        url += f"&logo={logo}&logoColor={logo_color}"
    return url


def normalize_badge_svg(svg: str, label: str) -> str:
    """Ensure visible label text uses real spaces, never %20."""
    display = label.upper()
    svg = svg.replace("%20", " ")
    svg = re.sub(
        r'(font-weight="bold">)[^<]+(<)',
        rf"\g<1>{display}\g<2>",
        svg,
        count=1,
    )
    svg = re.sub(
        r'(aria-label=")[^"]+(")',
        rf'\g<1>{display}\2',
        svg,
        count=1,
    )
    svg = re.sub(
        r"(<title>)[^<]+(</title>)",
        rf"\g<1>{display}\g<2>",
        svg,
        count=1,
    )
    return svg


def groq_icon_data_uri() -> str:
    inner = (
        '<svg fill="#c48a7a" role="img" viewBox="0 0 24 24" '
        'xmlns="http://www.w3.org/2000/svg"><title>Groq</title>'
        f'<g transform="translate(1.4,1.4) scale(0.102)"><path d="{GROQ_PATH}"/></g></svg>'
    )
    compact = re.sub(r">\s+<", "><", inner)
    encoded = base64.b64encode(compact.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def build_groq_badge() -> str:
    icon = groq_icon_data_uri()
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="86" height="28" role="img" aria-label="GROQ">'
        "<title>GROQ</title>"
        '<g shape-rendering="crispEdges"><rect width="86" height="28" fill="#363b44"/></g>'
        '<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" '
        'text-rendering="geometricPrecision" font-size="100">'
        f'<image x="9" y="7" width="14" height="14" href="{icon}"/>'
        '<text transform="scale(.1)" x="530" y="175" textLength="370" font-weight="bold">GROQ</text>'
        "</g></svg>"
    )


def main() -> None:
    for filename, label, logo, logo_color in BADGES:
        url = badge_url(label, logo, logo_color)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        svg = normalize_badge_svg(data.decode("utf-8"), label)
        out = BADGE_DIR / filename
        out.write_text(svg, encoding="utf-8")
        print(f"saved: {filename} ({len(svg)} bytes)")

    groq_path = BADGE_DIR / "groq.svg"
    groq_path.write_text(build_groq_badge(), encoding="utf-8")
    print(f"saved: groq.svg (custom icon, {groq_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
