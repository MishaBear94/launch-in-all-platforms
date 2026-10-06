#!/usr/bin/env python3
"""Extract the outbound "Featured on" / badge links from a page.

Usage: discover_featured_on.py <page-url> [--out links.json]

Finds the section whose text contains "Featured on" / "As seen on" (or, failing
that, every <a> wrapping an <img> that points off-site), reads the platform name
from aria-label, title or img alt, and dedupes by href (marquee strips render
the list twice). Prints a markdown table and optionally writes JSON.
"""
import html, json, re, sys, urllib.request
from urllib.parse import urlparse

if len(sys.argv) < 2:
    sys.exit(__doc__)
url = sys.argv[1]
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
host = urlparse(url).netloc.removeprefix('www.')

# Prefer the block around the "Featured on" label; fall back to the whole page.
m = re.search(r'(featured on|as seen on|featured in)', page, re.I)
scope = page
if m:
    start = page.rfind('<section', 0, m.start())
    start = start if start != -1 else max(0, m.start() - 2000)
    end = page.find('</section>', m.end())
    scope = page[start:end if end != -1 else m.end() + 200000]

rows, seen = [], set()
for a in re.finditer(r'<a\b([^>]*)>(.*?)</a>', scope, re.S | re.I):
    attrs, inner = a.group(1), a.group(2)
    href_m = re.search(r'href="([^"]+)"', attrs)
    if not href_m or '<img' not in inner.lower():
        continue
    href = html.unescape(href_m.group(1))
    dom = urlparse(href).netloc.removeprefix('www.')
    if not dom or dom == host or href in seen:
        continue
    seen.add(href)
    label = re.search(r'(?:aria-label|title)="([^"]+)"', attrs)
    alt = re.search(r'alt="([^"]*)"', inner)
    src = re.search(r'src="([^"]+)"', inner)
    name = html.unescape((label or alt).group(1)) if (label or alt) else dom
    name = re.sub(r'^(Featured on|Listed on|Verified on|Launched on|As seen on)\s+', '', name).strip() or dom
    rows.append({'name': name, 'domain': dom, 'href': href,
                 'deep_link': bool(urlparse(href).path.strip('/')),
                 'img': html.unescape(src.group(1)) if src else ''})

print(f'{len(rows)} unique links, {len({r["domain"] for r in rows})} domains\n')
print('| # | Platform | Domain | Link target | URL |\n|---|---|---|---|---|')
for i, r in enumerate(rows, 1):
    print(f"| {i} | {r['name']} | {r['domain']} | {'listing page' if r['deep_link'] else 'homepage'} | {r['href']} |")
if out:
    json.dump(rows, open(out, 'w'), ensure_ascii=False, indent=1)
