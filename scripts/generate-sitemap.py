#!/usr/bin/env python3
"""Generate sitemap.xml for bulletdodgelee.github.io from HTML pages.

Usage: python3 scripts/generate-sitemap.py
Run from anywhere; the repo root is derived from this file's location.
"""
import os
import re
from datetime import datetime, timezone

BASE_URL = "https://zombiewarlee.github.io"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT = os.path.join(REPO_ROOT, "sitemap.xml")

# Google Search Console verification files (e.g. google5a133824844edada.html)
GSC_RE = re.compile(r"^google[0-9a-fA-F]+\.html$")

def find_html_pages(root):
    pages = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            if not name.endswith(".html"):
                continue
            if GSC_RE.match(name):
                continue
            pages.append(os.path.join(dirpath, name))
    return sorted(pages)

def build_urlset(pages):
    urls = []
    for page in pages:
        rel = os.path.relpath(page, REPO_ROOT)
        if rel == "index.html":
            loc = f"{BASE_URL}/"
            priority = "1.0"
        else:
            loc = f"{BASE_URL}/{rel.replace(os.sep, '/')}"
            priority = "0.8"
        lastmod = datetime.fromtimestamp(os.path.getmtime(page), tz=timezone.utc).strftime("%Y-%m-%d")
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>""")
    return "\n".join(urls)

def main():
    pages = find_html_pages(REPO_ROOT)
    urlset = build_urlset(pages)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urlset}\n"
        "</urlset>\n"
    )
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Generated {OUTPUT} with {len(pages)} URL(s).")

if __name__ == "__main__":
    main()
