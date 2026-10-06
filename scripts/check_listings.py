#!/usr/bin/env python3
"""Refresh a launch ledger from the public listing pages (logged out, like a visitor).

Usage: scripts/check_listings.py launches/<p>/listings.yaml [--discover] [--write]

For each listing: open the public page with headless Chromium, record whether it is live
(shows the product name, no 404), whether it has a vote button, and the visible vote count.
--discover  fill missing listing_url from data/platforms.yaml `listing` patterns and the
            platform's sitemap.xml (pages whose URL contains the product slug)
--write     save results back into the YAML (`live`, `votes`, `upvote`, `checked`)
Requires: pip install playwright pyyaml && playwright install chromium
"""
import asyncio, datetime, os, re, sys, urllib.request
import yaml
from playwright.async_api import async_playwright

ROOT = os.path.join(os.path.dirname(__file__), '..')
VOTE_RE = r'up-?vote|\bvotes?\b|▲|squeeze'

def registry():
    return {p['id']: p for p in yaml.safe_load(open(os.path.join(ROOT, 'data', 'platforms.yaml')))}

def sitemap_hit(base, slug):
    try:
        x = urllib.request.urlopen(urllib.request.Request(base.rstrip('/') + '/sitemap.xml', headers={'User-Agent': 'Mozilla/5.0'}), timeout=20).read().decode('utf-8', 'replace')
        m = re.search(r'<loc>([^<]*' + re.escape(slug) + r'[^<]*)</loc>', x, re.I)
        return m.group(1) if m else None
    except Exception:
        return None

async def check(ctx, sem, l, name):
    async with sem:
        p = await ctx.new_page()
        try:
            r = await p.goto(l['listing_url'], timeout=30000, wait_until='domcontentloaded')
            try:
                await p.wait_for_load_state('networkidle', timeout=8000)
            except Exception:
                pass
            await p.wait_for_timeout(1500)
            txt = await p.evaluate("(document.querySelector('main')||document.body).innerText")
            has_name = re.search(re.escape(name), txt, re.I) is not None
            l['live'] = bool(r and r.status < 400 and has_name)
            btns = await p.evaluate("""(re) => [...document.querySelectorAll('button,a,[role=button]')].filter(e=>e.offsetParent)
                .map(e=>((e.getAttribute('aria-label')||'')+' '+e.innerText).replace(/\\s+/g,' ').trim())
                .filter(t=>new RegExp(re,'i').test(t) && !/customer support/i.test(t) && t.length<60)""", VOTE_RE)
            # drop vote buttons that belong to *other* products listed on the page ("Upvote Foo", "Squeeze Foo")
            def other(b):
                m = re.search(r'(?i:up-?vote|squeeze|vote for)\s+(?!this\b|•|—|-|\d)([A-Z][\w.+-]*)', b)
                return bool(m) and not re.search(re.escape(name), b, re.I)
            own = [b for b in btns if not other(b)]
            nums = [int(n) for b in own for n in re.findall(r'\b(\d{1,4})\b', b) if int(n) < 1900]
            m = re.search(r'\b(\d{1,4})\s*(?:up)?votes?\b', txt[:3000], re.I)
            l['upvote'] = bool(own) or bool(re.search(r'upvotes? (open|unlock)', txt, re.I))
            l['votes'] = nums[0] if nums else (int(m.group(1)) if own and m and int(m.group(1)) < 1900 else None)
        except Exception as e:
            l['live'] = None
            l['error'] = str(e)[:80]
        l['checked'] = datetime.date.today().isoformat()
        await p.close()

async def main(path, discover, write):
    d = yaml.safe_load(open(path))
    reg = registry()
    name = d.get('product_name') or d.get('product')
    slug = d.get('slug') or d.get('product')
    domain = re.sub(r'^https?://(www\.)?', '', d.get('site', '')).strip('/')
    for l in d['listings']:
        if l.get('listing_url') or not discover:
            continue
        p = reg.get(l['platform'], {})
        if p.get('listing'):
            l['listing_url'] = p['listing'].replace('{slug}', slug).replace('{domain}', domain)
        hit = sitemap_hit(p.get('url', ''), slug) if p.get('url') else None
        if hit:
            l['listing_url'] = hit
    todo = [l for l in d['listings'] if l.get('listing_url') and l.get('status') != 'skipped']
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36')
        sem = asyncio.Semaphore(8)
        await asyncio.gather(*[check(ctx, sem, l, name) for l in todo])
        await b.close()
    for l in todo:
        print(f"{l['platform']:<18} live={l.get('live')!s:<5} upvote={l.get('upvote')!s:<5} votes={l.get('votes')!s:<4} {l['listing_url']} {l.get('error','')}")
    if write:
        yaml.safe_dump(d, open(path, 'w'), sort_keys=False, allow_unicode=True, width=200)
        print(f'\nwrote {path}')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    asyncio.run(main(a[0], '--discover' in a, '--write' in a))
